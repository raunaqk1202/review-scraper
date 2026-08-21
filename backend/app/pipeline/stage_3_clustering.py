import uuid
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.pipeline.base import PipelineStage
from app.models.feedback import FeedbackItem
from app.models.clusters import Cluster, ClusterMembership

# Use sklearn's HDBSCAN (available in 1.3+) and sentence-transformers
from sklearn.cluster import HDBSCAN
from sentence_transformers import SentenceTransformer

class Stage3Clustering(PipelineStage):
    def __init__(self):
        super().__init__()
        # Load the BGE model as requested
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        
    @property
    def stage_name(self) -> str:
        return "Semantic Clustering"
        
    @property
    def stage_number(self) -> int:
        return 3

    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        self.logger.info("Starting Stage 3: Semantic Clustering")
        
        # Get items that have been cleaned but not yet clustered
        # In a real pipeline, we'd check if they are already in a cluster
        # For MVP, we'll cluster all valid items
        query = select(FeedbackItem).where(
            FeedbackItem.is_spam == False,
            FeedbackItem.cleaned_text != None
        )
        result = await db.execute(query)
        items = result.scalars().all()
        
        if len(items) < 5:
            self.logger.warning("Not enough items to cluster. Need at least 5.")
            return {"status": "skipped", "reason": "not_enough_data"}
            
        metrics = {
            "items_clustered": len(items),
            "clusters_created": 0,
            "noise_items": 0
        }
        
        # 1. Generate embeddings
        texts = [item.cleaned_text for item in items]
        embeddings = self.model.encode(texts)
        
        # 2. Cluster using HDBSCAN
        # min_cluster_size=3 as per architecture
        clusterer = HDBSCAN(min_cluster_size=3, metric='euclidean')
        labels = clusterer.fit_predict(embeddings)
        
        # 3. Group items by cluster label
        clusters_map: Dict[int, List[FeedbackItem]] = {}
        for idx, label in enumerate(labels):
            if label == -1:
                metrics["noise_items"] += 1
                continue # Noise
            if label not in clusters_map:
                clusters_map[label] = []
            clusters_map[label].append(items[idx])
            
        # 4. Save clusters to DB
        for label, cluster_items in clusters_map.items():
            # In a real app, we'd call an LLM to generate a label based on the cluster_items texts.
            # For this MVP step, we'll generate a generic label or extract top words.
            cluster_name = f"Auto-Cluster {label}"
            
            new_cluster = Cluster(
                id=str(uuid.uuid4()),
                label=cluster_name,
                description=f"Generated cluster containing {len(cluster_items)} items.",
                theme="General",
                member_count=len(cluster_items),
                cohesion_score=0.85 # Placeholder
            )
            db.add(new_cluster)
            
            for item in cluster_items:
                membership = ClusterMembership(
                    cluster_id=new_cluster.id,
                    feedback_item_id=item.id,
                    similarity_score=0.9
                )
                db.add(membership)
                
            metrics["clusters_created"] += 1
            
        await db.commit()
        return metrics

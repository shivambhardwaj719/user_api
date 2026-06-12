from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

def check_references_and_get_deletable_instances(db: Session, model_class, ids: list[int]):
    instances = db.query(model_class).filter(model_class.id.in_(ids)).all()
    if not instances:
        return [], []

    mapper = inspect(model_class)
    references_details = []
    deletable_instances = []

    for instance in instances:
        is_referenced = False
        
        for rel in mapper.relationships:
            related_attr = getattr(instance, rel.key)
            if related_attr:
                if rel.uselist:
                    active_items = [i for i in related_attr if getattr(i, 'deleted_by', None) is None]
                    if active_items:
                        is_referenced = True
                        references_details.append({
                            'related_model': rel.mapper.class_.__name__,
                            'related_objects': [str(item) for item in active_items[:5]]
                        })
                else:
                    item = related_attr
                    if getattr(item, 'deleted_by', None) is None:
                        is_referenced = True
                        references_details.append({
                            'related_model': rel.mapper.class_.__name__,
                            'related_objects': [str(item)]
                        })
                        
        if not is_referenced:
            deletable_instances.append(instance)

    return deletable_instances, references_details

from publish import publish
from sword.settings import RABBITMQ_EXCHANGE, RABBITMQ_ROUTING_KEY


def publish_performed_task(task):
    message = {
        "id": task.id,
        "user": task.user.id,
        "performed_at": task.performed_at.isoformat() if task.performed_at else None,
    }

    # TODO read these from configuration file
    publish(
        exchange=RABBITMQ_EXCHANGE,
        routing_key=RABBITMQ_ROUTING_KEY,
        message=message,
    )


def on_task_post_save(sender, instance, created, **kwargs):
    if not created and instance.performed_at:
        publish_performed_task(task=instance)

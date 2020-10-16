class Notify:
    """Notify class implements all notifications from one instance to all
    instance owners.
    """

    def __init__(self):
        """__init__ initializes Notify instance.
        """
        pass

    @staticmethod
    def notify(instance, notification):
        for owner in instance.owner:
            if hasattr(owner, "notify"):
                owner.notify(instance, notification)

from rosgraph_monitor.observer import TopicObserver
from std_msgs.msg import Bool
from diagnostic_msgs.msg import DiagnosticStatus, KeyValue


class ObjetiveErrorObserver(TopicObserver):
    def __init__(self, name):
        topics = [("/obj_error", Bool)]     # list of pairs

        super(ObjetiveErrorObserver, self).__init__(
            name, 10, topics)

    def calculate_attr(self, msgs):
        status_msg = DiagnosticStatus()

        attr = str("False")
        if msgs[0].data:
            attr = str("True")

        status_msg = DiagnosticStatus()
        status_msg.level = DiagnosticStatus.OK
        status_msg.name = self._id
        status_msg.values.append(
            KeyValue("objetive_error", attr))
        status_msg.message = "QA status"

        return status_msg

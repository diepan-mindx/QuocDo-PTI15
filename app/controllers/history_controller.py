from models.history import History
from DAO import DAO  # Handles JSON data storage


class HistoryController:
    def __init__(self):
        self.__history_list = []
        self.__generate_history_list()

    # Private methods (only used within this class)
    def __generate_history_list(self):
        # Load history data from JSON
        self.__convert_dict_to_objects()  # Convert to History objects

    def __convert_dict_to_objects(self):
        dict_list = DAO.load_json_data("history")
        self.__history_list = [
            History(
                id=history["id"],
                time=history["time"],
                created_by=history["created_by"],
                type_name=history["type"],
            )
            for history in dict_list
        ]  # Convert each dictionary to a History object

    def __convert_histories_to_dict(self):
        return [
            {
                "id": history.get_id(),
                "time": history.get_time(),
                "created_by": history.get_created_by(),
                "type": history.get_type(),
            }
            for history in self.__history_list
        ]

    def __save_in_data(self):
        # Save history data to JSON
        DAO.save_json_data("history", self.__convert_histories_to_dict())

    def find_best(self, email):
        histories_by_creator = self.search_by_creator(email)
        return min([float(item.get_time()) for item in histories_by_creator], default=0)

    def find_worst(self, email):
        histories_by_creator = self.search_by_creator(email)
        return max([float(item.get_time()) for item in histories_by_creator], default=0)

    # Create: Add a new history entry
    def add_history(self, history: History):
        new_id = len(self.__history_list) + 1  # Generate new ID
        history.set_id(new_id)
        self.__history_list.append(history)
        self.__save_in_data()

    # Read: Search history by ID
    def search_by_id(self, history_id):
        for history in self.__history_list:
            if history.get_id() == history_id:
                return history
        return None  # History not found

    # Read: Search history by created_by (email)
    def search_by_creator(self, email):
        return [
            history
            for history in self.__history_list
            if history.get_created_by() == email
        ]

    # Update: Update a history record by ID
    def update_history(self, updated_history: History):
        for i, history in enumerate(self.__history_list):
            if history.get_id() == updated_history.get_id():
                self.__history_list[i] = updated_history
                self.__save_in_data()
                return

    # Delete: Delete a history record by ID
    def delete_history(self, history_id):
        self.__history_list = [
            history for history in self.__history_list if history.get_id() != history_id
        ]
        self.__save_in_data()

    # Sorting functions
    def sort_by_id(self):
        self.__history_list.sort(key=lambda history: history.get_id())

    def sort_by_time(self):
        self.__history_list.sort(key=lambda history: history.get_time())

    def sort_by_created_by(self):
        self.__history_list.sort(key=lambda history: history.get_created_by())

    def sort_by_type(self):
        self.__history_list.sort(key=lambda history: history.get_type())

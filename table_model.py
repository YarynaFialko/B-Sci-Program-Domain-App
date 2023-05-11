from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal

class TableModel(QAbstractTableModel):
    dataChanged = pyqtSignal(QModelIndex, QModelIndex)
    layoutChanged = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self._data = data

        self._header_labels = ["Student ID", "Grade"]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data[row][column]
            return str(value)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    # def headerData(self, section, orientation, role):
    #     if role == Qt.DisplayRole:
    #         if orientation == Qt.Horizontal:
    #             return f"Column {section}"
    #         else:
    #             return f"Row {section}"

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header_labels[section]
        return None

    def updateData(self, data_in):
        self._data = data_in
        self.layoutChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))

    def updateHeaderLabels(self, header_labels_in):
        self._header_labels = header_labels_in
        self.layoutChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        
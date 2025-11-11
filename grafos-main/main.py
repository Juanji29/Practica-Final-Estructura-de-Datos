import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from grafos_ui import Ui_MainWindow
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem


class Nodo(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, id, app):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)  # Dibujar el nodo centrado
        self.setBrush(QtGui.QBrush(QtGui.QColor("lightblue")))
        self.setPen(QtGui.QPen(QtCore.Qt.black))
        self.id = id
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)
        self.text_item = QGraphicsTextItem(f"Nodo {self.id}", self)
        self.text_item.setPos(-10, -10)  # Ajusta la posición del texto para que no se superponga con el nodo
        self.app = app  # Referencia a la aplicación para actualizar las aristas
        self.aristas = []  # Para guardar las aristas conectadas a este nodo

    def agregar_arista(self, arista):
        self.aristas.append(arista)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Cuando se mueva el nodo, actualizar las aristas
            for arista in self.aristas:
                arista.actualizar_posiciones()
        return super().itemChange(change, value)


class Arista(QGraphicsLineItem):
    def __init__(self, nodo1, nodo2, peso, scene):
        super().__init__()
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso = peso
        self.scene = scene

        # Agregar el peso de la arista como un texto
        self.text_item = QGraphicsTextItem(str(self.peso))
        self.scene.addItem(self.text_item)

        # Agregar la línea y actualizar posiciones
        self.actualizar_posiciones()

        # Establecer el evento de clic para engrosar la arista y los nodos conectados
        self.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.setPen(QtGui.QPen(QtCore.Qt.black))

    def actualizar_posiciones(self):
        x1, y1 = self.nodo1.scenePos().x(), self.nodo1.scenePos().y()
        x2, y2 = self.nodo2.scenePos().x(), self.nodo2.scenePos().y()

        # Actualizar la línea de la arista
        self.setLine(x1, y1, x2, y2)

        # Colocar el texto en el centro de la línea
        self.text_item.setPos((x1 + x2) / 2, (y1 + y2) / 2)

    def mousePressEvent(self, event):
        # Engrosar la línea y los nodos conectados al hacer clic en la arista
        self.setPen(QtGui.QPen(QtCore.Qt.red, 3))  # Cambia el color y grosor de la arista
        self.nodo1.setPen(QtGui.QPen(QtCore.Qt.red, 3))  # Engrosar el nodo1
        self.nodo2.setPen(QtGui.QPen(QtCore.Qt.red, 3))  # Engrosar el nodo2
        super().mousePressEvent(event)  # Llama al evento de clic original


class GrafoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(GrafoApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Crear un QLabel
        self.lblTitulo2 = QtWidgets.QLabel(self)
        self.lblTitulo2.setGeometry(10, 10, 100, 100)  # Ajusta la posición y tamaño del QLabel

        # Cargar la imagen
        pixmap = QtGui.QPixmap("Recurso-1-8.png")

        # Redimensionar la imagen (por ejemplo, a 100x100 píxeles)
        pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)

        # Usar el graphicsView existente
        self.graphicsView = self.ui.graphicsView

        # Configurar la escena del QGraphicsView
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        # Conectar el botón para generar el grafo
        self.ui.btnPintarGrafo.clicked.connect(self.dibujar_grafo)

        # Conectar el botón para calcular Dijkstra
        self.ui.btnDjikstra.clicked.connect(self.calcular_dijkstra)


        # Conectar el clic en la barra de título del QTableWidget para llenar con valores aleatorios
        self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.llenar_matriz_aleatoria)

        # Lista para almacenar los nodos y las aristas
        self.nodos = []
        self.aristas = []

    def dibujar_grafo(self):
        try:
            # Limpiar la escena y listas
            self.scene.clear()
            self.nodos.clear()
            self.aristas.clear()

            # Obtener la nueva matriz de la UI y dibujar el grafo
            matriz = self.obtener_matriz()

            # Dibujar nodos y aristas
            self.dibujar_nodos_y_aristas(matriz)
        except Exception as e:
            print(f"Error al dibujar el grafo: {e}")

    def obtener_matriz(self):
        try:
            filas = self.ui.tableWidget.rowCount()
            columnas = self.ui.tableWidget.columnCount()
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    item = self.ui.tableWidget.item(i, j)
                    valor = int(item.text()) if item and item.text().isdigit() else 0
                    fila.append(valor)
                matriz.append(fila)
            return matriz
        except Exception as e:
            print(f"Error al obtener la matriz: {e}")
            return []

    def dibujar_nodos_y_aristas(self, matriz):
        try:
            num_nodos = len(matriz)
            radius = 20

            # Definir los límites para la posición aleatoria de los nodos
            width = self.graphicsView.width() - 100
            height = self.graphicsView.height() - 100

            # Dibujar nodos
            for i in range(num_nodos):
                x = random.randint(50, width)  # Coordenada x aleatoria
                y = random.randint(50, height)  # Coordenada y aleatoria
                nodo = Nodo(x, y, radius, i + 1, self)
                nodo.setPos(x, y)  # Posicionar el nodo en la escena
                self.scene.addItem(nodo)
                self.nodos.append(nodo)

            # Dibujar aristas
            for i in range(num_nodos):
                for j in range(i + 1, num_nodos):
                    peso = matriz[i][j]
                    if peso > 0:
                        nodo1 = self.nodos[i]
                        nodo2 = self.nodos[j]

                        # Crear y agregar arista
                        arista = Arista(nodo1, nodo2, peso, self.scene)
                        self.aristas.append(arista)
                        self.scene.addItem(arista)

                        # Agregar aristas a los nodos para que se actualicen al moverlos
                        nodo1.agregar_arista(arista)
                        nodo2.agregar_arista(arista)

        except Exception as e:
            print(f"Error al dibujar nodos y aristas: {e}")

    def llenar_matriz_aleatoria(self, index):
        """Llena toda la matriz con valores aleatorios entre 0 y 100, con 0 en las diagonales."""
        try:
            filas = self.ui.tableWidget.rowCount()
            columnas = self.ui.tableWidget.columnCount()

            for i in range(filas):
                for j in range(columnas):
                    if i == j:
                        self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem('0'))  # No aristas a sí mismo
                    else:
                        valor_aleatorio = random.randint(1, 100)  # Valor aleatorio entre 1 y 100
                        self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor_aleatorio)))
        except Exception as e:
            print(f"Error al llenar la matriz: {e}")

    

    def calcular_dijkstra(self):
        try:
            # Obtener el nodo inicial desde el QLineEdit
            nodo_inicial = int(self.ui.lineEditNodoInicial.text()) - 1  # Restar 1 porque los índices son 0-based
            if nodo_inicial < 0 or nodo_inicial >= len(self.nodos):
                print("El nodo inicial está fuera de rango.")
                return

            # Ejecutar el algoritmo de Dijkstra
            self.dijkstra(nodo_inicial)
        except ValueError:
            print("Por favor, introduce un número válido para el nodo inicial.")


    def dijkstra(self, nodo_inicial):
        try:
            # Obtener la matriz de adyacencia
            matriz = self.obtener_matriz()
            num_nodos = len(matriz)

            # Inicializar las distancias y el conjunto de nodos visitados
            distancias = [float('inf')] * num_nodos
            distancias[nodo_inicial] = 0
            visitados = [False] * num_nodos
            predecesores = [-1] * num_nodos  # Para rastrear el camino

            for _ in range(num_nodos):
                # Encontrar el nodo no visitado con la distancia mínima
                min_distancia = float('inf')
                nodo_actual = -1
                for i in range(num_nodos):
                    if not visitados[i] and distancias[i] < min_distancia:
                        min_distancia = distancias[i]
                        nodo_actual = i

                if nodo_actual == -1:  # Si no hay nodo alcanzable, salir
                    break

                # Marcar el nodo actual como visitado
                visitados[nodo_actual] = True

                # Actualizar las distancias a los nodos vecinos
                for vecino in range(num_nodos):
                    peso = matriz[nodo_actual][vecino]
                    if peso > 0 and not visitados[vecino]:
                        nueva_distancia = distancias[nodo_actual] + peso
                        if nueva_distancia < distancias[vecino]:
                            distancias[vecino] = nueva_distancia
                            predecesores[vecino] = nodo_actual

            # Mostrar los resultados en el QLabel
            resultados = "Distancias desde el nodo :\n"
            for i, distancia in enumerate(distancias):
                resultados += f"Nodo {nodo_inicial + 1} -> Nodo {i + 1}: {distancia if distancia != float('inf') else 'Inalcanzable'}\n"

            resultados += "\nCaminos más cortos:\n"
            for destino in range(num_nodos):
                if distancias[destino] != float('inf'):
                    camino = []
                    actual = destino
                    while actual != -1:
                        camino.insert(0, actual + 1)
                        actual = predecesores[actual]
                    resultados += f"Camino al nodo {destino + 1}: {' -> '.join(map(str, camino))}\n"

            # Mostrar los resultados en el QLabel
            self.ui.labelResultados.setText(resultados)

        except Exception as e:
            self.ui.labelResultados.setText(f"Error en el algoritmo de Dijkstra: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GrafoApp()
    window.show()
    sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
import speech_recognition as sr

MENUES = ["ARCHIVO", "TAMAÑO", "COLORES", "AYUDA"]
SUB1 = [[("BORRAR", "B"), ("GUARDAR", "G")],
       [("1px", "U"), ("3px", "T"), ("5px", "I"), ("7px", "S"), ("9px", "N")],
       [("AMARILLO", "A"), ("AZUL", "Z"), ("ROJO", "R"), ("VERDE", "V"), ("VIOLETA", "L"), ("NARANJA", "N"), ("MAGENTA", "M"), ("ESMERALDA", "E"), ("BLANCO", "W"), ("NEGRO", "K")],
       [("DOCUMENTACION", "X"), ("AYUDA", "Y")]]
COLQT = [Qt.yellow, Qt.blue, Qt.red, Qt.green, QColor(128, 0, 128), QColor(255, 128, 0), Qt.magenta, QColor(0, 184, 139), Qt.white, Qt.black]
COLOR_DEFECTO = "NEGRO"
TAMAÑO_DEFECTO = 5
COLORES = dict(zip([tupla[0] for tupla in SUB1[2]], COLQT))
MENUES_INSTANCIAS = {}

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 400
        width = 800
        height = 600

        icon = "icons/pain.png"

        self.setWindowTitle("LIENZO VIRTUAL")
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.black

        self.lastPoint = QPoint()






        BARRA = self.menuBar()
        
        for i in MENUES:
            menu = QMenu(i, self)
            BARRA.addMenu(menu)
            MENUES_INSTANCIAS[i] = menu
        
        for i, submenu in enumerate(SUB1):
            for nombre, atajo in submenu:
                accion = QAction(QIcon("icons/" + nombre.lower().capitalize() + ".png"), nombre, self)
                accion.setShortcut("Ctrl+" + atajo)

            
                MENUES_INSTANCIAS[MENUES[i]].addAction(accion)


                
                if nombre[0].isdigit():
                    accion.triggered.connect(self.conectar_tampincel(nombre))
                elif i == 2:
                    accion.triggered.connect(self.conectar_seleccionacolor(nombre))
                else:
                    accion.triggered.connect(eval("self." + nombre.lower()))
                        
        button = QPushButton(self)
        button.setText("Iniciar reconocimiento de voz")
        button.setGeometry(100, 50, 200, 50)
        button.clicked.connect(self.reconocimiento_de_voz)

    def conectar_tampincel(self, nom):
        return lambda: self.tampincel(nom[0])

    def conectar_seleccionacolor(self, nom):
        return lambda: self.seleccionacolor(nom)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def guardar(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

    def borrar(self):
        self.image.fill(Qt.white)
        self.update()

    def tampincel(self, tam):
        try:
            print("esto es lo que esta pasandole a tamaño: ", tam)
            self.brushSize = int(tam)
        except:
            self.brushSize = int(TAMAÑO_DEFECTO)

    def seleccionacolor(self, color):
        try:
            print("esto es lo que esta pasandole a color: ", color)
            self.brushColor = COLORES[color.upper()]
        except:
            self.brushColor = COLORES[COLOR_DEFECTO]

    def documentacion(self):
        pass

    def ayuda(self):
        pass

    def reconocimiento_de_voz(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Di algo...")
            audio = r.listen(source)
        try:
            texto = r.recognize_google(audio, language='es')
            print("Has dicho: " + texto)
            self.reconocedor(texto.split())
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio")
        except sr.RequestError as e:
            print("Error al realizar la solicitud; {0}".format(e))

    def reconocedor(self, comandos): # ["Tamaño", "3"]
        if (comandos[0].lower() == "tamaño"):
            self.tampincel(comandos[1].lower())
        elif (comandos[0].lower() == "color"):
            self.seleccionacolor(comandos[1])
        elif (comandos[0].lower() == "archivo") and (comandos[1].lower() in ["guardar"]):
            self.guardar()
        elif (comandos[0].lower() == "archivo") and (comandos[1].lower() in ["borrar"]):
            self.borrar()
        else:
            print("solo esta reconociendo esto:", comandos)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
    sys.exit(app.exec())

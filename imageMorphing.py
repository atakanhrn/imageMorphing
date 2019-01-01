import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog, QHBoxLayout, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################





class App(QMainWindow):
    box1 = QGroupBox
    box2 = QGroupBox
    box3 = QGroupBox
    hor_lay = QVBoxLayout
    targetImageOpen = False
    secondImageOpen = False
    points1 = []
    points2 = []

    def __init__(self):

        self.points1 = [(2, 0), (145, 2), (318, 3), (318, 240), (316, 474), (158, 477), (2, 474), (50, 120), (197, 87), (199, 231), (50, 196), (242, 173), (44, 285), (151, 278), (272, 290), (104, 327), (67, 360), (125, 411), (201, 401), (243, 361)]         ### To hard-code the points
        self.points2 = [(2, 0), (149, 0), (317, 1), (317, 235), (315, 473), (158, 478), (2, 475), (65, 102), (220, 86), (201, 224), (52, 183), (244, 170), (55, 276), (136, 285), (279, 268), (105, 329), (70, 346), (139, 400), (194, 386), (224, 354)]
        self.alpha = 0.5
        QMainWindow.__init__(self)
        self.setup_main_window()
        self.set_window_layout()
        self.initUI()
    def setup_main_window(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Image Morphing")

    def set_window_layout(self):
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.box1 = QGroupBox("Input image")
        self.box2 = QGroupBox("Target image")
        self.box3 = QGroupBox("Morphed image")
        self.hor_lay = QHBoxLayout()
        self.hor_lay.addWidget(self.box1)
        self.hor_lay1 = QHBoxLayout()
        self.hor_lay1.addWidget(self.box2)
        self.hor_lay2 = QHBoxLayout()
        self.hor_lay2.addWidget(self.box3)
        self.horizontalLayout.addLayout(self.hor_lay)
        self.horizontalLayout.addLayout(self.hor_lay1)
        self.horizontalLayout.addLayout(self.hor_lay2)
        layout = QHBoxLayout()
        self.box1.setLayout(layout)
        layout2 = QHBoxLayout()
        self.box2.setLayout(layout2)
        layout3 = QHBoxLayout()
        self.box3.setLayout(layout3)

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        openInputImage = QAction('Open Input Image', self)
        openTargetImage = QAction('Open Target Image', self)
        exit = QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        fileMenu.addAction(openInputImage)
        fileMenu.addAction(openTargetImage)
        fileMenu.addAction(exit)
        removePoints = QAction('Points are currently hard-coded. Click to remove selected points.', self)
        undoLastClick = QAction('Undo last click', self)
        self.toolbar = self.addToolBar('Create Triangulation')
        createTriangulation = QAction('Create Triangulation', self)
        morph = QAction('Morph', self)
        self.toolbar.addAction(createTriangulation)
        self.toolbar.addAction(morph)
        self.toolbar.addAction(removePoints)


        openInputImage.triggered.connect(self.openInputImage)
        openTargetImage.triggered.connect(self.openTargetImage)
        #exit.triggered.connect(app.exit())
        createTriangulation.triggered.connect(self.createTriangulation)
        morph.triggered.connect(self.morph)
        removePoints.triggered.connect(self.removePoints)

        self.show()

    def removePoints(self):
        self.points1.clear()
        self.points2.clear()

    def openInputImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.inputFileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.inputFileName:
            print(self.inputFileName)
        self.inputImage = cv2.imread(self.inputFileName, cv2.IMREAD_COLOR)
        self.inputImageOpen = True
        self.size1 = self.inputImage.shape
        print(self.size1)
        rect1 = (0, 0, self.size1[1], self.size1[0])
        self.subDiv1 = cv2.Subdiv2D(rect1)
        self.img1 = QImage(self.inputFileName)
        self.label1 = QLabel(self)
        pixmap = QPixmap(self.inputFileName)
        self.label1.setPixmap(pixmap)
        self.box1.layout().addWidget(self.label1)
        self.label1.setAlignment(Qt.AlignTop)
        self.show()
        self.label1.mousePressEvent = self.getPosImg1

    def openTargetImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.targetFileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.targetFileName:
            print(self.targetFileName)

        self.targetImage = cv2.imread(self.targetFileName, cv2.IMREAD_COLOR)
        self.targetImageOpen = True
        # cv2.namedWindow("main window")
        # lay = QVBoxLayout()
        self.size2 = self.targetImage.shape
        print(self.size1)
        rect2 = (0, 0, self.size2[1], self.size2[0])
        self.subDiv2 = cv2.Subdiv2D(rect2)
        self.label2 = QLabel(self)
        pixmap = QPixmap(self.targetFileName)
        self.label2.setPixmap(pixmap)
        #label.resize(pixmap.width(), pixmap.height())
        self.box2.layout().addWidget(self.label2)
        self.label2.setAlignment(Qt.AlignTop)

        self.show()
        self.label2.mousePressEvent = self.getPosImg2

    def getPosImg1(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.points1.append((x,y))
        print(self.points1)

    def getPosImg2(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.points2.append((x,y))
        print(self.points2)

    # Check if a point is inside a rectangle
    def rect_contains(self, rect, point):
        if point[0] < rect[0]:
            return False
        elif point[1] < rect[1]:
            return False
        elif point[0] > rect[2]:
            return False
        elif point[1] > rect[3]:
            return False
        return True

    # Draw a point
    def draw_point(self, img, p, color):
        cv2.circle(img, p, 2, color)

    # Draw delaunay triangles
    def draw_delaunay(self, img, subdiv, color):
        triangleList = subdiv.getTriangleList()
        triangleCornerList = []
        size = img.shape
        r = (0, 0, size[1], size[0])
        print('draw function')
        print(triangleList)
        for t in triangleList:

            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])
            print('triangle list')
            if self.rect_contains(r, pt1) and self.rect_contains(r, pt2) and self.rect_contains(r, pt3):
                #print('inside if')
                cv2.line(img, pt1, pt2, color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt2, pt3, color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt3, pt1, color, 1, cv2.LINE_AA, 0)
                triangleCornerList.append([pt1,pt2,pt3])

        return triangleCornerList


    def createTriangulation(self):

        if self.inputImageOpen == True:
            self.inputImageOrj = self.inputImage.copy()     ##copy image so that do not lose original
            for point in self.points1:
                self.draw_point(self.inputImage, point, (255, 0, 0))
                self.subDiv1.insert(point)
            self.triangleCornerList1 = self.draw_delaunay(self.inputImage, self.subDiv1, (255,255,255))
            triangulatedInputFileName = 'triangulatedInputFile.jpg'
            cv2.imwrite(triangulatedInputFileName, self.inputImage)

        if self.targetImageOpen ==True:
            self.targetImageOrj = self.targetImage.copy()       ##copy image so that do not lose original
            for point in self.points2:
                self.draw_point(self.targetImage, point, (0, 0, 255))
                self.subDiv2.insert(point)
            self.triangleCornerList2 = self.draw_delaunay(self.targetImage, self.subDiv2, (255, 255, 255))
            triangulatedTargetFileName = 'triangulatedTargetImage.jpg'
            cv2.imwrite(triangulatedTargetFileName, self.targetImage)
        pixmap = QPixmap(triangulatedInputFileName)             ##update image
        self.label1.setPixmap(pixmap)
        self.label1.update()

        pixmap = QPixmap(triangulatedTargetFileName)            ##update image
        self.label2.setPixmap(pixmap)
        self.label2.update()
        print("create triangulation")

    def morph(self):
        if len(self.points1) != len(self.points2):
            if len(self.points1) > len(self.points2):
                print('More points selected from first image. Cannot morph yet')
                return
            elif len(self.points2) > len(self.points1):
                print('More points selected from second image. Cannot morph yet')
                return
        R, C, B = self.inputImage.shape
        self.resultImage = np.zeros((R, C, B), np.uint8)
        outputTriangleCornerList = []
        for index in range(len(self.triangleCornerList1)):
            ## self.morphTriangle(self.triangleCornerList1[index], self.triangleCorList2[index])          ## if triangle corners come in the order I give the points, this line can be used
            ## following line is used instead of the above to handle following of the corresponding points. The order in points array, i.e the order we click on the images matter!!!
            self.morphTriangle(self.triangleCornerList1[index], (self.points2[self.points1.index(self.triangleCornerList1[index][0])], self.points2[self.points1.index(self.triangleCornerList1[index][1])], self.points2[self.points1.index(self.triangleCornerList1[index][2])]))
        label = QLabel(self)
        fileName = 'result.jpg'
        cv2.imwrite(fileName, self.resultImage)         ## save the morphed image
        pixmap = QPixmap(fileName)
        label.setPixmap(pixmap)
        self.box3.layout().addWidget(label)
        label.setAlignment(Qt.AlignTop)

        self.show()

    def morphTriangle(self, triangleList1, triangleList2):
        affineTransformMatrix = self.findAffineTransformMatrix(triangleList1, triangleList2)
        x, y, w, h = cv2.boundingRect(np.float32([triangleList2]))
        invAffineTransformMatrix = np.linalg.inv(affineTransformMatrix)
        R, C, B = self.inputImage.shape
        outputImg = np.zeros((R, C, B), np.uint8)
        for x_coord in range(x, x+w):
            for y_coord in range(y, y+h):
                if x_coord>320 or y_coord>480:
                    continue
                outputCoord = np.matmul(invAffineTransformMatrix, [[x_coord],
                                                  [y_coord],
                                                  [1]      ]   )
                if outputCoord[0]>320 or outputCoord[1]>480:
                    continue
                #print(outputCoord)
                #if outputImg[y_coord,x_coord,0] == 0 and outputImg[y_coord,x_coord,1] == 0 and outputImg[y_coord,x_coord,2]==0:
                if self.resultImage[y_coord, x_coord, 0] == 0 and self.resultImage[y_coord, x_coord, 1] == 0 and self.resultImage[y_coord, x_coord, 2] == 0:        ##fill in rectangle
                    outputImg[y_coord,x_coord,0] = self.inputImageOrj[int(outputCoord[1]),int(outputCoord[0]),0]
                    outputImg[y_coord,x_coord,1] = self.inputImageOrj[int(outputCoord[1]),int(outputCoord[0]),1]
                    outputImg[y_coord,x_coord,2] = self.inputImageOrj[int(outputCoord[1]),int(outputCoord[0]),2]
        mask = np.zeros((R, C, 3), dtype=np.uint8)
        pts = np.array(((int(triangleList2[0][0]), int(triangleList2[0][1])),
                        (int(triangleList2[1][0]), int(triangleList2[1][1])),
                        (int(triangleList2[2][0]), int(triangleList2[2][1]))), dtype=np.int32)
        cv2.fillConvexPoly(mask, pts, (1.0, 1.0, 1.0), 0, 0)        ## mask by triangle corners
        outputImg = outputImg * mask
        self.resultImage = self.resultImage + outputImg


    def findAffineTransformMatrix(self, triangleList1, triangleList2):
        x1 = int(triangleList1[0][0])
        x2 = int(triangleList1[1][0])
        x3 = int(triangleList1[2][0])
        y1 = int(triangleList1[0][1])
        y2 = int(triangleList1[1][1])
        y3 = int(triangleList1[2][1])
        M = [[x1, y1, 1, 0, 0, 0],
             [0, 0, 0, x1, y1, 1],
             [x2, y2, 1, 0, 0, 0],
             [0, 0, 0, x2, y2, 1],
             [x3, y3, 1, 0, 0, 0],
             [0, 0, 0, x3, y3, 1]]
        x1out = int(triangleList2[0][0])
        x2out = int(triangleList2[1][0])
        x3out = int(triangleList2[2][0])
        y1out = int(triangleList2[0][1])
        y2out = int(triangleList2[1][1])
        y3out = int(triangleList2[2][1])
        q = [x1out, y1out, x2out, y2out, x3out, y3out]
        unknownsMatrix = np.matmul(np.linalg.inv(M), q)
        a11 = unknownsMatrix[0]
        a12 = unknownsMatrix[1]
        a13 = unknownsMatrix[2]
        a21 = unknownsMatrix[3]
        a22 = unknownsMatrix[4]
        a23 = unknownsMatrix[5]
        affineTransformMatrix = [[a11, a12, a13],
                                 [a21, a22, a23],
                                 [0, 0, 1]]
        return affineTransformMatrix

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.setAccessibleName("main window")
    sys.exit(app.exec_())

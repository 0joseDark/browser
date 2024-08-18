import sys
import os
from PyQt5.QtCore import QUrl, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget, 
                             QVBoxLayout, QListWidget, QDialog, QPushButton, QFileDialog, 
                             QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem

# Classe para gerenciar favoritos
class FavoritesManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Favorites Manager")
        self.setGeometry(400, 400, 300, 400)
        self.layout = QVBoxLayout()

        # Lista de favoritos
        self.favorites_list = QListWidget()
        self.load_favorites()
        self.layout.addWidget(self.favorites_list)

        # Botão para abrir o favorito selecionado
        self.open_button = QPushButton("Open Favorite")
        self.open_button.clicked.connect(self.open_favorite)
        self.layout.addWidget(self.open_button)

        # Botão para remover o favorito selecionado
        self.remove_button = QPushButton("Remove Favorite")
        self.remove_button.clicked.connect(self.remove_favorite)
        self.layout.addWidget(self.remove_button)

        self.setLayout(self.layout)

    def load_favorites(self):
        # Carrega os favoritos do arquivo 'favorites.txt'
        self.favorites_list.clear()
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as f:
                for line in f:
                    self.favorites_list.addItem(line.strip())

    def open_favorite(self):
        # Abre o favorito selecionado
        selected_item = self.favorites_list.currentItem()
        if selected_item:
            self.accept()

    def remove_favorite(self):
        # Remove o favorito selecionado do arquivo e da lista
        selected_item = self.favorites_list.currentItem()
        if selected_item:
            with open('favorites.txt', 'r') as f:
                lines = f.readlines()
            with open('favorites.txt', 'w') as f:
                for line in lines:
                    if line.strip() != selected_item.text():
                        f.write(line)
            self.load_favorites()

# Classe para gerenciar o histórico de navegação
class HistoryManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History Manager")
        self.setGeometry(400, 400, 300, 400)
        self.layout = QVBoxLayout()

        # Lista de histórico
        self.history_list = QListWidget()
        self.load_history()
        self.layout.addWidget(self.history_list)

        # Botão para abrir a página do histórico selecionada
        self.open_button = QPushButton("Open History")
        self.open_button.clicked.connect(self.open_history)
        self.layout.addWidget(self.open_button)

        # Botão para limpar todo o histórico
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self.clear_history)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)

    def load_history(self):
        # Carrega o histórico do arquivo 'history.txt'
        self.history_list.clear()
        if os.path.exists('history.txt'):
            with open('history.txt', 'r') as f:
                for line in f:
                    self.history_list.addItem(line.strip())

    def open_history(self):
        # Abre a página do histórico selecionada
        selected_item = self.history_list.currentItem()
        if selected_item:
            self.accept()

    def clear_history(self):
        # Limpa todo o histórico
        with open('history.txt', 'w') as f:
            f.write('')
        self.load_history()

# Classe para gerenciar as configurações avançadas
class SettingsManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings Manager")
        self.setGeometry(400, 400, 300, 200)
        self.layout = QVBoxLayout()

        # Placeholder para futuras configurações avançadas
        self.layout.addWidget(QPushButton("Advanced Setting 1"))
        self.layout.addWidget(QPushButton("Advanced Setting 2"))
        self.layout.addWidget(QPushButton("Advanced Setting 3"))

        self.setLayout(self.layout)

# Classe principal do navegador
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Browser with Advanced Features")
        self.setGeometry(100, 100, 1200, 800)

        # Gerenciamento de abas
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.add_new_tab)  # Adiciona nova aba ao dar duplo clique na barra de abas
        self.tabs.currentChanged.connect(self.update_url)  # Atualiza a URL na barra de navegação quando a aba muda
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)  # Fecha a aba quando solicitado

        self.setCentralWidget(self.tabs)

        # Barra de navegação
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Botão de voltar
        back_btn = QAction(QIcon('back.png'), "Back", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.navbar.addAction(back_btn)

        # Botão de avançar
        forward_btn = QAction(QIcon('forward.png'), "Forward", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navbar.addAction(forward_btn)

        # Botão de recarregar
        reload_btn = QAction(QIcon('reload.png'), "Reload", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.navbar.addAction(reload_btn)

        # Botão de início
        home_btn = QAction(QIcon('home.png'), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        # Campo de URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # Botão de adicionar favoritos
        fav_btn = QAction(QIcon('fav.png'), "Add to Favorites", self)
        fav_btn.triggered.connect(self.add_favorite)
        self.navbar.addAction(fav_btn)

        # Botão de abrir favoritos
        open_fav_btn = QAction(QIcon('open_fav.png'), "Open Favorites", self)
        open_fav_btn.triggered.connect(self.show_favorites_manager)
        self.navbar.addAction(open_fav_btn)

        # Botão de abrir histórico
        history_btn = QAction(QIcon('history.png'), "History", self)
        history_btn.triggered.connect(self.show_history_manager)
        self.navbar.addAction(history_btn)

        # Botão de configuração
        settings_btn = QAction(QIcon('settings.png'), "Settings", self)
        settings_btn.triggered.connect(self.show_settings_manager)
        self.navbar.addAction(settings_btn)

        # Adicionar uma nova aba ao iniciar o navegador
        self.add_new_tab(QUrl("http://www.google.com"), "Homepage")

    def add_new_tab(self, qurl=None, label="New Tab"):
        # Adiciona uma nova aba ao navegador
        if qurl is None:
            qurl = QUrl("http://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

        # Conecta o gerenciador de downloads
        browser.page().profile().downloadRequested.connect(self.download_requested)

        # Registra a URL no histórico
        browser.urlChanged.connect(self.record_history)

    def close_current_tab(self, i):
        # Fecha a aba atual se houver mais de uma aberta
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_home(self):
        # Navega para a página inicial
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        # Navega para a URL digitada na barra de navegação
        url = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, i):
        # Atualiza a URL na barra de navegação e o título da janela
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def update_title(self, browser):
        # Atualiza o título da janela com o título da página atual
        title = browser.page().title()
        self.setWindowTitle(f"{title} - Python Browser")

    def update_urlbar(self, qurl, browser=None):
        # Atualiza a barra de URL com o endereço da página atual
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(qurl.toString())

    def add_favorite(self):
        # Adiciona a página atual aos favoritos
        url = self.tabs.currentWidget().url().toString()
        with open('favorites.txt', 'a') as f:
            f.write(url + '\n')
        QMessageBox.information(self, "Favorites", "Page added to favorites!")

    def show_favorites_manager(self):
        # Exibe o gerenciador de favoritos
        favorites_manager = FavoritesManager(self)
        if favorites_manager.exec_() == QDialog.Accepted:
            selected_url = favorites_manager.favorites_list.currentItem().text()
            self.tabs.currentWidget().setUrl(QUrl(selected_url))

    def show_history_manager(self):
        # Exibe o gerenciador de histórico
        history_manager = HistoryManager(self)
        if history_manager.exec_() == QDialog.Accepted:
            selected_url = history_manager.history_list.currentItem().text()
            self.tabs.currentWidget().setUrl(QUrl(selected_url))

    def show_settings_manager(self):
        # Exibe o gerenciador de configurações
        settings_manager = SettingsManager(self)
        settings_manager.exec_()

    def record_history(self, qurl):
        # Registra a URL no histórico
        with open('history.txt', 'a') as f:
            f.write(qurl.toString() + '\n')

    def download_requested(self, download):
        # Gerencia o processo de download
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if path:
            download.setPath(path)
            download.accept()

# Executa o aplicativo
app = QApplication(sys.argv)
QApplication.setApplicationName("Python Browser with Advanced Features")
window = Browser()
window.show()
sys.exit(app.exec_())
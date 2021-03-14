from PySide2.QtWidgets import QInputDialog
from paragon.model.game import Game

from paragon.ui.controllers.dialogue_editor import DialogueEditor
from paragon.ui.controllers.chapter_editor import ChapterEditor
from paragon.ui.controllers.fe13_avatar_config_window import FE13AvatarConfigWindow
from paragon.ui.views.ui_fe13_main_widget import Ui_FE13MainWidget


class FE13MainWidget(Ui_FE13MainWidget):
    def __init__(self, ms, gs, main_window):
        super().__init__()
        self.gs = gs
        self.ms = ms
        self.main_window = main_window

        self.dialogue_editors = {}
        self.chapter_editor = None
        self.avatar_editor = None

        self.chapters_button.clicked.connect(self._on_chapters)
        self.characters_button.clicked.connect(self._on_characters)
        self.items_button.clicked.connect(self._on_items)
        self.skills_button.clicked.connect(self._on_skills)
        self.classes_button.clicked.connect(self._on_classes)
        self.armies_button.clicked.connect(self._on_armies)
        self.tiles_button.clicked.connect(self._on_tiles)
        self.asset_definitions_button.clicked.connect(self._on_asset_definitions)
        self.presets_button.clicked.connect(self._on_presets)
        self.portraits_button.clicked.connect(self._on_portraits)
        self.edit_dialogue_button.clicked.connect(self._on_edit_dialogue)
        self.configure_avatar_button.clicked.connect(self._on_configure_avatar)
        self.sprite_data_button.clicked.connect(self._on_bmap_icons)
        self.gmap_button.clicked.connect(self._on_gmap)

    def _on_chapters(self):
        # TODO: Error handling.
        if self.chapter_editor:
            self.chapter_editor.show()
        else:
            self.gs.data.set_store_dirty("gamedata", True)
            self.chapter_editor = ChapterEditor(self.ms, self.gs)
            self.chapter_editor.show()

    def _on_characters(self):
        self.main_window.open_node_by_id("characters")

    def _on_items(self):
        self.main_window.open_node_by_id("items")

    def _on_skills(self):
        self.main_window.open_node_by_id("skills")

    def _on_classes(self):
        self.main_window.open_node_by_id("classes")

    def _on_armies(self):
        self.main_window.open_node_by_id("belong")

    def _on_tiles(self):
        self.main_window.open_node_by_id("tiles")

    def _on_asset_definitions(self):
        self.main_window.open_node_by_id("asset_definitions")

    def _on_presets(self):
        self.main_window.open_node_by_id("preset_asset_definitions")

    def _on_portraits(self):
        self.main_window.open_node_by_id("facedata")

    def _on_bmap_icons(self):
        self.main_window.open_node_by_id("bmap_icons")

    def _on_gmap(self):
        self.main_window.open_node_by_id("gmap_placements")

    def _on_edit_dialogue(self):
        choices = self.gs.data.enumerate_text_archives()
        choice, ok = QInputDialog.getItem(self, "Select Text", "Path", choices, 0)
        if ok:
            if choice in self.dialogue_editors:
                self.dialogue_editors[choice].show()
            else:
                editor = DialogueEditor(
                    self.gs.data, self.gs.dialogue, self.gs.sprite_animation, Game.FE13
                )
                editor.set_archive(choice, False)
                self.dialogue_editors[choice] = editor
                editor.show()

    def _on_configure_avatar(self):
        if not self.avatar_editor:
            self.avatar_editor = FE13AvatarConfigWindow(self.ms, self.gs)
        self.avatar_editor.show()

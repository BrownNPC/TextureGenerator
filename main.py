
import flet as ft
from PIL import Image
import time
import os

class TextureManager:
    
    def __init__(self) -> None:
        
        self.template = Image.new("RGBA", (385,385))
        self._faces = {
            "front": (0, 0),
            "left": (0, 128),
            "top": (0, 256),
            "right": (128, 0),
            "bottom": (128, 128),
            "back": (128, 256)
        }
    def add_texture(self, texture_path:str, face_name:str):
        face_name= face_name.lower()
        """
        face_name can be "front", "left", "top", "right", "bottom", "back"
        """
        if face_name not in self._faces:
            raise ValueError("face_name must be one of 'front', 'left', 'top', 'right', 'bottom', 'back'")
        
        tex = Image.open(texture_path).resize((129,129))
        self.template.paste(tex, self._faces[face_name])

    def save(self, path:str):
        self.template.save(path)


def main(page:ft.Page):
    page.window.max_height = 1920
    page.window.max_width = 400
    page.title = "Texture Combinator 9001"
    page.update()

    tm = TextureManager()
    

    all_faces_same = False
    prev_open_path = os.path.expanduser("~")
    def toggle_all_faces_same(e):
        nonlocal all_faces_same
        all_faces_same = not all_faces_same
        page.update()
    
    images_row = ft.Row(
        [],
        scroll=True,
        spacing=2,
        width=400,
        
        alignment=ft.MainAxisAlignment.CENTER
        
    )

    def fileHandler(e):
        
        FP = ft.FilePicker()
        page.add(FP)
        def on_result(e:ft.FilePickerResultEvent):
            nonlocal prev_open_path
            prev_open_path = e.files[-1].path.strip(e.files[-1].name) # remove file name from path
            for file in e.files:
                # print(file.path)
                images_row.controls.append(
                    ft.Draggable(
                        ft.Image(
                            file.path,
                            width=64,
                            height=64,
                            fit=ft.ImageFit.FILL,
                            filter_quality=ft.FilterQuality.NONE
                        )
                    )
                )
            page.update()
        FP.on_result = on_result

        FP.pick_files("Import your textures", allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE, initial_directory=prev_open_path)

    def drag_will_accept(e):
        e.control.content.border = ft.border.all(
            2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
        )
        e.control.update()

    def drag_accept(e: ft.DragTargetAcceptEvent):
        src = page.get_control(e.src_id)
        e.control.content.content = ft.Image(
            src.content.src,
            width=64,
            height=64,
            fit=ft.ImageFit.FILL,
            filter_quality=ft.FilterQuality.NONE
        )
        
        e.control.content.border = None
        page.update()

        def get_face_name():
            # access the "Face" column on the FaceTable (datatable below)
            # check the same row, and get the face
            return e.control.parent.parent.cells[0].content.value
        
        tm.add_texture(src.content.src, get_face_name())
        # print(get_face_name())

    
    
    FaceTable = ft.DataTable(
        columns= [ft.DataColumn(ft.Text("Face", size=22)), ft.DataColumn(ft.Text("Texture", size=22))],
        
        data_row_max_height=float("inf"),
        rows=[
            # front face
            ft.DataRow (
                
                cells=[
                    ft.DataCell(ft.Text("Front", size=18)),
                    ft.DataCell(
                        
                        ft.DragTarget(
                        on_will_accept=drag_will_accept, on_accept=drag_accept,
                        content=ft.Container(
                            width=64,
                            height=64,
                            bgcolor=ft.colors.BLUE_GREY_100,
                            margin=5,
                            
                            border_radius=5)
                    ))

                ]
            ),
            # back face
            ft.DataRow (
                cells=[
                    ft.DataCell(ft.Text("Back", size=18)),
                    ft.DataCell(
                        ft.DragTarget(ft.Container(
                        width=64,
                        height=64,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        margin=5,
                        border_radius=5,
                        ),
                    on_will_accept=drag_will_accept, on_accept=drag_accept)),
                    
                ]
            ),
            # left face
            ft.DataRow (
                cells=[
                    ft.DataCell(ft.Text("Left", size=18)),
                    ft.DataCell(
                        ft.DragTarget(
                        
                        on_will_accept=drag_will_accept, on_accept=drag_accept,
                        content=ft.Container(
                            width=64,
                            height=64,
                            bgcolor=ft.colors.BLUE_GREY_100,
                            margin=5,
                            border_radius=5)
                    ))

                ]
            ),
            # Right
            ft.DataRow (
                cells=[
                    ft.DataCell(ft.Text("Right", size=18)),
                    ft.DataCell(
                        ft.DragTarget(
                        on_will_accept=drag_will_accept, on_accept=drag_accept,
                        content=ft.Container(
                            width=64,
                            height=64,
                            bgcolor=ft.colors.BLUE_GREY_100,
                            margin=5,
                            border_radius=5)
                    ))

                ]
            ),
            # Top
            ft.DataRow (
                cells=[
                    ft.DataCell(ft.Text("Top", size=18)),
                    ft.DataCell(
                        ft.DragTarget(
                        on_will_accept=drag_will_accept, on_accept=drag_accept,
                        content=ft.Container(
                            width=64,
                            height=64,
                            
                            bgcolor=ft.colors.BLUE_GREY_100,
                            margin=5,
                            border_radius=5)
                    ))

                ]
            ),
            # Bottom
            ft.DataRow (
                cells=[
                    ft.DataCell(ft.Text("Bottom", size=18)),
                    ft.DataCell(
                        ft.DragTarget(
                        on_will_accept=drag_will_accept, on_accept=drag_accept,
                        content=ft.Container(
                            width=64,
                            height=64,
                            bgcolor=ft.colors.BLUE_GREY_100,
                            margin=5,
                            border_radius=5)
                    ))

                ]
            ),
            
        ],
    )


    def export(e):

        def get_image_from_face(face:str):
            faces = {
                "front": 0,
                "back": 1,
                "left": 2,
                "right": 3,
                "top": 4,
                "bottom": 5
            }
            
            return FaceTable.rows[faces[face]].cells[1].content.content.content
        # get the image from the front face
        def open_save_diag_and_save():
            save_diag.save_file("Export your textures", "Texture.png",
                             file_type= ft.FilePickerFileType.CUSTOM, allowed_extensions=["png"],
                             )

        save_diag = ft.FilePicker(on_result=lambda e: tm.save(e.path))
        page.add(save_diag)
        if all_faces_same:
            first_face = get_image_from_face("front") 
            if not first_face:
                page.open(
                    ft.AlertDialog(title=ft.Text('The "Front" face is empty. \nPlease drag an image on the Front face.')))
                # page.update()
                return
            tm.add_texture(first_face.src, "front")
            tm.add_texture(first_face.src, "back")
            tm.add_texture(first_face.src, "left")
            tm.add_texture(first_face.src, "right")
            tm.add_texture(first_face.src, "top")
            tm.add_texture(first_face.src, "bottom")
            open_save_diag_and_save()
            return
        
        for face in ["front", "back", "left", "right", "top", "bottom"]:
            image = get_image_from_face(face)
            if not image:
                page.open(
                    ft.AlertDialog(title=ft.Text(f'The "{face}" face is empty. \nPlease drag an image on the {face} face.')))
                # page.update()
                return
            tm.add_texture(image.src, face)
        open_save_diag_and_save()

        
        
    


    ExportButton = ft.TextButton("Export!",ft.icons.SAVE_ALT_ROUNDED, on_click=export)

    page.add(
        ft.Column(
            [

            ft.Text("Texture Combinator 9001!!!!", size=24,text_align=ft.TextAlign.CENTER),
            ft.Divider(opacity=0),
            # ft.TextButton("Import Images", ft.icons.FILE_OPEN, on_click=fileHandler),
            ExportButton,
            ft.Text("Imported Images:", size=18),
            ft.Divider(opacity=0,height=2),
            images_row,
            ft.FilledButton("Import Images", on_click=fileHandler),
            ft.Divider(opacity=0,height=2),
            
            FaceTable,
            ft.Checkbox("Use Same Texture for All Faces",on_change=toggle_all_faces_same, tooltip="The texture in the Front slot will be used for all the other faces"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        
    )
    

    page.scroll = True
    page.update()

    
ft.app(target=main)
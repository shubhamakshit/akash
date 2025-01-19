from rich.console import Console
from rich.table import Table
from Endpoint import Endpoint
from glv import Global


class Package(dict):

    class Course:

        def __init__(self, data):
            self.id = data['id']
            self.slug = data['slug']
            self.name = data['name']

        def __str__(self):
            return self.name

        def __dict__(self):
            return {
                "id" : self.id,
                "slug" : self.slug,
                "name" : self.name
            }

    def __init__(self ,data):



        self.id = data['id']
        self.name = data['title']
        self.courses = [Package.Course(course) for course in data['courses']]
        super().__init__({
            "id": self.id,
            "name": self.name,
            "courses": [course.__dict__() for course in self.courses]
        })


    def __str__(self):
        return f"""
            Package: {self.name}
            ID: {self.id}
            Courses: {', '.join([str(course) for course in self.courses])}
            
"""

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "courses": [course.__dict__() for course in self.courses]
        }

    def to_console_table(self):
        table = Table(title=self.name, width=Global.term_col()-20)
        table.add_column("ID")
        table.add_column("Slug")
        table.add_column("Name")
        for course in self.courses:
            table.add_row(
                str(course.id),
                course.slug,
                course.name
            )
        return table


class Chapter(dict):

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        super().__init__({
            "id": self.id,
            "name": self.name
        })

    def __str__(self):
        return f"""
            Chapter: {self.name}
            ID: {self.id}
        """

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def to_console_table(self):
        table = Table(title=self.name, width=Global.term_col()-20)
        table.add_column("ID")
        table.add_column("Name")
        table.add_row(
            str(self.id),
            self.name
        )
        return table

class Chapters(list):

    def __init__(self, data):
        super().__init__([Chapter(chapter) for chapter in data])

    def __str__(self):
        return f"""
            CHAPTERS: {', '.join([str(chapter) for chapter in self])}
        """

    def __dict__(self):
        return [chapter.__dict__() for chapter in self]

    def to_console_table(self):
        table = Table(title="CHAPTERS", width=Global.term_col()-20)
        table.add_column("ID")
        table.add_column("Name")
        for chapter in self:
            table.add_row(
                str(chapter.id),
                chapter.name
            )
        return table


class ChapterComplete(dict):

    class Asset(list):
        def __init__(self, data):
            self.id = data['id']
            self.name = data['title']
            super().__init__([self.id, self.name])
            # super().__init__([ChapterComplete.Asset(data) for data in data['assets']])

        def __dict__(self):
            return {
                "id": self.id,
                "name": self.name
            }

    class Assets:
        def __init__(self,asset_type,data):
            self.type = asset_type
            self.objects = [ChapterComplete.Asset(asset) for asset in data]

        def __dict__(self):
            return {
                "type": self.type,
                "objects": self.objects
            }

    def __init__(self, data):
        self.id = data['id']

        self.list_of_assets = [ChapterComplete.Assets(asset_type,asset) for asset_type,asset in data['assets'].items()]
        super().__init__(
            {
                "id": self.id,
                "assets": [asset.__dict__() for asset in self.list_of_assets]
            }
        )

    def to_console_table(self):
        table = Table(title="CHAPTER", width=Global.term_col()-20)
        table.add_column("ID")
        table.add_column("Assets")


        for assets in self.list_of_assets:
            print("Asset : ", assets.type)
            assets_table = Table(title=assets.type, width=Global.term_col()-20)

            assets_table.add_column("ID")
            assets_table.add_column("Name")

            for asset in assets.objects:
                assets_table.add_row(
                    str(asset.id),
                    asset.name
                )

            table.add_row(
                str(self.id),
                assets_table
            )
        return table


class Endpoints:
    URLS = {
        'PACKAGES': 'https://session-service.aakash.ac.in/prod/chl/api/v1/itutor/package/',
        'USER': 'https://session-service.aakash.ac.in/prod/sess/api/v1/user/',
    }

    def __init__(self, access_token, client_id="a6fbf1d2-27c3-46e1-b149-0380e506b763"):
        self.access_token = access_token
        self.client_id = client_id
        self.headers = {
            'access-token': self.access_token,
            'x-client-id': self.client_id
        }





    def PACKAGES(self):
        return Endpoint(
            url=Endpoints.URLS['PACKAGES'],
            method='GET',
            headers=self.headers,
            post_function=lambda data: [
                Package(package) for package in data['data']['packages']
            ]
        )

    def USER(self):
        return Endpoint(
            url=Endpoints.URLS['USER'],
            method='GET',
            headers=self.headers
        )

    def CHAPTERS(self, package_id, course_id):
        return Endpoint(
            url=f"https://session-service.aakash.ac.in/prod/chl/api/v1/itutor/package/{package_id}/subject/?course_id={course_id}",
            method='GET',
            headers=self.headers,
            post_function=lambda data: Chapters(data['data']['chapters'])
        )


    def CHAPTER(self, package_id, course_id, chapter_id):
        return Endpoint(
            url=f"https://session-service.aakash.ac.in/prod/chl/api/v2/itutor/package/{package_id}/course/{course_id}/chapter/?node_id={chapter_id}",
            method='GET',
            headers=self.headers,
            post_function=lambda data: ChapterComplete(data['data']['chapter'])
        )

    def ASSET(self, package_id, course_id, chapter_id, asset_id, asset_type="ebook"):
        return Endpoint(
        url=f"https://session-service.aakash.ac.in/prod/chl/api/v1/itutor/package/{package_id}/course/{course_id}/chapter/{chapter_id}/asset/{asset_id}/?asset_type={asset_type}",
            method='GET',
            headers=self.headers
        )
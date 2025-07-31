import io

import frappe
from frappe import _
from frappe.core.doctype.file.file import File
from frappe.integrations.google_oauth import GoogleOAuth
from googleapiclient.http import MediaIoBaseDownload

SUPPORTED_MIME_TYPES = frozenset(
	[
		# Hình ảnh
		"image/jpeg",
		"image/jpg",
		"image/png",
		"image/gif",
		"image/bmp",
		"image/tiff",
		"image/webp",
		"image/svg+xml",
		"image/ico",
		# Tài liệu văn bản
		"text/plain",
		"text/csv",
		"text/html",
		"text/xml",
		"application/rtf",
		# Microsoft Office
		"application/msword",  # .doc
		"application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
		"application/vnd.ms-excel",  # .xls
		"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
		"application/vnd.ms-powerpoint",  # .ppt
		"application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
		# PDF
		"application/pdf",
		# OpenDocument
		"application/vnd.oasis.opendocument.text",  # .odt
		"application/vnd.oasis.opendocument.spreadsheet",  # .ods
		"application/vnd.oasis.opendocument.presentation",  # .odp
		# Archive files
		"application/zip",
		"application/x-rar-compressed",
		"application/x-7z-compressed",
		# Google Apps files
		"application/vnd.google-apps.document",
		"application/vnd.google-apps.spreadsheet",
		"application/vnd.google-apps.presentation",
		"application/vnd.google-apps.drawing",
	]
)

SUPPORTED_EXTENSIONS = frozenset(
	[
		# Hình ảnh
		"jpg",
		"jpeg",
		"png",
		"gif",
		"bmp",
		"tiff",
		"webp",
		"svg",
		"ico",
		# Văn bản
		"txt",
		"csv",
		"html",
		"xml",
		"rtf",
		# Microsoft Office
		"doc",
		"docx",
		"xls",
		"xlsx",
		"ppt",
		"pptx",
		# PDF
		"pdf",
		# OpenDocument
		"odt",
		"ods",
		"odp",
		# Archive
		"zip",
		"rar",
		"7z",
	]
)

EXPORT_FORMATS = {
	"application/vnd.google-apps.document": {
		"mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		"extension": ".docx",
	},
	"application/vnd.google-apps.spreadsheet": {
		"mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		"extension": ".xlsx",
	},
	"application/vnd.google-apps.presentation": {
		"mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
		"extension": ".pptx",
	},
	"application/vnd.google-apps.drawing": {"mime_type": "image/png", "extension": ".png"},
	"application/vnd.google-apps.script": {
		"mime_type": "application/vnd.google-apps.script+json",
		"extension": ".json",
	},
	"application/vnd.google-apps.site": {"mime_type": "text/plain", "extension": ".txt"},
	"application/vnd.google-apps.form": {"mime_type": "application/zip", "extension": ".zip"},
	"application/vnd.google-apps.map": {"mime_type": "application/pdf", "extension": ".pdf"},
}


class InnoFile(File):
	def custom_sync_google_drive(self):
		try:
			service = self.get_google_drive_service()
			if not service:
				frappe.msgprint("Unable to connect to Google Drive", indicator="red")
				return

			total_folders, total_files = self.sync_folders_recursive(service, "root", "Home")
			frappe.msgprint(
				f"Sync complete! Processed {total_folders} folders and {total_files} files.",
				indicator="green",
			)
		except Exception as e:
			error_msg = f"Error while synchronizing: {e}"
			frappe.msgprint(error_msg, indicator="red")

	def get_google_drive_service(self):
		try:
			google_settings = frappe.get_single("Google Drive")

			if not google_settings.refresh_token:
				raise Exception("Missing Refresh Token in Google Drive settings")

			google_oauth = GoogleOAuth(domain="drive", validate=True)

			access_token = google_settings.get_access_token()
			if not access_token:
				token_response = google_oauth.refresh_access_token(google_settings.refresh_token)
				if token_response and "access_token" in token_response:
					access_token = token_response["access_token"]
				else:
					raise Exception("Unable to refresh access token")

			service = google_oauth.get_google_service_object(
				access_token=access_token, refresh_token=google_settings.refresh_token
			)

			return service

		except Exception:
			return None

	def sync_folders_recursive(self, service, parent_folder_id="root", erpnext_parent_folder="Home", level=0):
		total_folders = 0
		total_files = 0

		try:
			if level > 10:
				return total_folders, total_files

			files_count = self.download_files_from_google_drive(parent_folder_id, erpnext_parent_folder)
			total_files += files_count

			query = f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
			results = (
				service.files()
				.list(q=query, fields="files(id, name, parents, createdTime, modifiedTime)", pageSize=100)
				.execute()
			)

			folders = results.get("files", [])

			for folder in folders:
				folder_id = folder["id"]
				folder_name = folder["name"]

				erpnext_folder_name, is_new_folder = self.create_or_get_erpnext_folder(
					folder_name, erpnext_parent_folder, folder_id
				)

				if is_new_folder:
					total_folders += 1

				sub_folders, sub_files = self.sync_folders_recursive(
					service, folder_id, erpnext_folder_name, level + 1
				)
				total_folders += sub_folders
				total_files += sub_files

		except Exception as e:
			frappe.log_error(f"Error when syncing folders at level {level}: {e}", "Google Drive Folder Sync")

		return total_folders, total_files

	def create_or_get_erpnext_folder(self, folder_name, parent_folder, google_folder_id):
		try:
			existing_folder = frappe.db.exists(
				"File", {"file_name": folder_name, "folder": parent_folder, "is_folder": 1}
			)

			if existing_folder:
				return existing_folder, False

			new_folder = frappe.get_doc(
				{
					"doctype": "File",
					"file_name": folder_name,
					"is_folder": 1,
					"folder": parent_folder,
					"content": None,
					"file_url": f"https://drive.google.com/drive/folders/{google_folder_id}",
					"is_private": getattr(self, "is_private", 0),
				}
			)

			new_folder.insert()
			frappe.db.commit()

			return new_folder.name, True

		except Exception:
			return parent_folder, False

	def is_supported_file_type(self, mime_type, file_name):
		if mime_type in SUPPORTED_MIME_TYPES:
			return True

		file_extension = file_name.lower().split(".")[-1] if "." in file_name else ""

		return file_extension in SUPPORTED_EXTENSIONS

	def download_files_from_google_drive(self, folder_id, erpnext_folder_name):
		successful_downloads = 0

		try:
			google_settings = frappe.get_single("Google Drive")
			google_oauth = GoogleOAuth(domain="drive", validate=True)

			access_token = google_settings.get_access_token()
			if not access_token:
				token_response = google_oauth.refresh_access_token(google_settings.refresh_token)
				if token_response and "access_token" in token_response:
					access_token = token_response["access_token"]
				else:
					return successful_downloads

			service = google_oauth.get_google_service_object(
				access_token=access_token, refresh_token=google_settings.refresh_token
			)

			# Query để lấy tất cả file trong folder (loại trừ folders)
			query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
			results = (
				service.files()
				.list(q=query, fields="files(id, name, mimeType, size, exportLinks)", pageSize=100)
				.execute()
			)

			files = results.get("files", [])

			if not files:
				return successful_downloads

			failed_downloads = 0
			skipped_files = 0
			updated_files = 0

			for file in files:
				file_id = file["id"]
				file_name = file["name"]
				mime_type = file["mimeType"]
				final_file_name = file_name

				try:
					if not self.is_supported_file_type(mime_type, file_name):
						skipped_files += 1
						continue

					# Xử lý Google Apps files (docs, sheets, slides, etc.)
					if mime_type.startswith("application/vnd.google-apps."):
						file_content, final_file_name = self.export_google_apps_file(
							service, file_id, mime_type, file_name
						)
						if file_content is None:
							failed_downloads += 1
							continue
					else:
						try:
							request = service.files().get_media(fileId=file_id)
							file_stream = io.BytesIO()
							downloader = MediaIoBaseDownload(file_stream, request)
							done = False

							while not done:
								status, done = downloader.next_chunk()

							file_stream.seek(0)
							file_content = file_stream.read()

							if not file_content:
								failed_downloads += 1
								continue

						except Exception:
							failed_downloads += 1
							continue

					existing_file = frappe.db.exists(
						"File", {"file_name": final_file_name, "folder": erpnext_folder_name}
					)

					if existing_file:
						updated_files += 1
						continue

					new_file = frappe.get_doc(
						{
							"doctype": "File",
							"file_name": final_file_name,
							"is_folder": 0,
							"folder": erpnext_folder_name,
							"content": file_content,
							"file_type": mime_type,
							"is_private": getattr(self, "is_private", 0),
						}
					)

					new_file.insert()
					frappe.db.commit()
					successful_downloads += 1

				except Exception:
					failed_downloads += 1
					continue

		except Exception as e:
			frappe.log_error(
				f"Error downloading file from folder {folder_id}: {e}", "Google Drive File Download"
			)

		return successful_downloads

	def export_google_apps_file(self, service, file_id, mime_type, file_name):
		try:
			export_config = EXPORT_FORMATS.get(mime_type)

			if not export_config:
				frappe.log_error(f"Export is not supported for file types: {mime_type}", "Google Apps Export")
				return None, file_name

			export_mime_type = export_config["mime_type"]
			extension = export_config["extension"]

			# Thêm extension vào tên file nếu chưa có
			if not file_name.lower().endswith(extension.lower()):
				export_file_name = f"{file_name}{extension}"
			else:
				export_file_name = file_name

			# Export file
			request = service.files().export_media(fileId=file_id, mimeType=export_mime_type)
			file_stream = io.BytesIO()
			downloader = MediaIoBaseDownload(file_stream, request)
			done = False

			while not done:
				status, done = downloader.next_chunk()

			file_stream.seek(0)
			file_content = file_stream.read()

			if not file_content:
				return None, export_file_name

			return file_content, export_file_name

		except Exception:
			return None, file_name


@frappe.whitelist()
def sync_google_drive_folders():
	try:
		frappe.enqueue(
			enqueue_sync_google_drive_folders, queue="long", timeout=600, job_name="Sync Google Drive Folders"
		)

		frappe.msgprint(_("Syncing Google Drive folders in the background"), indicator="green")
	except Exception as e:
		frappe.log_error("Error during Google Drive sync", e)
		frappe.msgprint(_("Something wrong while trigger synchronization"), indicator="red")


def enqueue_sync_google_drive_folders():
	try:
		temp_file = InnoFile({"doctype": "File", "file_name": "temp_sync_file", "is_folder": 0})
		temp_file.custom_sync_google_drive()
	except Exception as e:
		frappe.log_error("Error during Google Drive sync", e)
		raise e

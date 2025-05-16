import tkinter as tk
from tkinter import filedialog
import requests
import os

def select_folder():
    default_dir = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'LocalLow', 'TVGS', 'Schedule I', 'Saves'
    )

    folder = filedialog.askdirectory(title="Select a Folder", initialdir=default_dir)
    if folder:
        selected_folder.set(folder)

def toggle_discord_settings():
    if discord_frame.winfo_viewable():
        discord_frame.pack_forget()
    else:
        discord_frame.pack(fill="x", padx=20, pady=(0, 20))

def download_files_from_channel():
    bot_token = bot_token_var.get()
    channel_id = channel_id_var.get()
    download_folder = selected_folder.get()

    if not bot_token or not channel_id:
        status_label.config(text="Bot token and channel ID must be set.")
        return

    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    params = {"limit": 50}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        status_label.config(text=f"Failed to fetch messages: {response.status_code}")
        return

    messages = response.json()
    os.makedirs(download_folder, exist_ok=True)
    count = 0

    for message in messages:
        attachments = message.get("attachments", [])
        for attachment in attachments:
            file_url = attachment["url"]
            file_name = attachment["filename"]
            file_data = requests.get(file_url, headers=headers)
            if file_data.status_code == 200:
                with open(os.path.join(download_folder, file_name), "wb") as f:
                    f.write(file_data.content)
                count += 1

    status_label.config(text=f"Downloaded {count} file(s).")

# Create main window
root = tk.Tk()
root.title("Folder and Discord File Downloader")
root.geometry("600x400")

selected_folder = tk.StringVar()
selected_folder.set("No folder selected.")

# --- Folder Selection ---
tk.Button(root, text="Select Folder", command=select_folder).pack(pady=(20, 10))
tk.Label(root, textvariable=selected_folder, wraplength=550, justify="left").pack(pady=(0, 10))

# --- Toggle Discord Settings ---
tk.Button(root, text="Discord Settings", command=toggle_discord_settings).pack(pady=(0, 10))

# --- Discord Settings Frame (initially hidden) ---
discord_frame = tk.Frame(root, borderwidth=1, relief="sunken")
discord_frame.pack_forget()  # Start hidden

bot_token_var = tk.StringVar()
channel_id_var = tk.StringVar()

tk.Label(discord_frame, text="Bot Token:").pack(anchor="w", padx=10, pady=(10, 0))
tk.Entry(discord_frame, textvariable=bot_token_var, width=60, show="*").pack(padx=10, pady=(0, 10))

tk.Label(discord_frame, text="Channel ID:").pack(anchor="w", padx=10)
tk.Entry(discord_frame, textvariable=channel_id_var, width=60).pack(padx=10, pady=(0, 10))

tk.Button(discord_frame, text="Download Files", command=download_files_from_channel).pack(pady=10)

# --- Status Label ---
status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=(0, 10))

# Start GUI
root.mainloop()

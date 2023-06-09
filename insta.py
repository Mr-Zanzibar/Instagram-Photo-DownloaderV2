import sys
import getpass
from colorama import Fore, Style
import instaloader
from pyfiglet import Figlet
from rich.console import Console
import tkinter as tk
from tkinter import messagebox

f = Figlet(font="banner3-D")
banner = f.renderText("Insta-Scraper")

# Create a rich console
console = Console()

# Print the title and an introduction
console.print(banner, "By Mr-Zanzibar, Don.Zanzibar#3562", style="bold green")

# create an instance of Instaloader
loader = instaloader.Instaloader()

# check if the target_username is provided as a command-line argument
if len(sys.argv) > 1:
    target_username = sys.argv[1]
else:
    target_username = input(Fore.WHITE + "Enter the " + Fore.RED + "target" + Fore.WHITE + " profile username: " + Style.RESET_ALL)

# prompt the user to enter the Instagram credentials
console.print("Enter your Instagram username:", style="blue", end=" ")
username = input()
console.print("Enter your Instagram password:", style="blue", end=" ")
password = getpass.getpass()

# Create a popup window
root = tk.Tk()
root.withdraw()

# Show a message box with the target username
result = messagebox.askquestion("Confirmation", f"Is '{target_username}' the correct target username?\nDo you want to download all the photos?")

if result == 'yes':
    try:
        # login to Instagram
        loader.login(username, password)

        # download the profile
        profile = instaloader.Profile.from_username(loader.context, target_username)
        loader.download_profile(profile, profile_pic=True)

        # download all the photos
        for post in profile.get_posts():
            if not post.is_video:
                loader.download_post(post, target=profile.username)

        console.print("Profile downloaded successfully.")

    except instaloader.exceptions.ProfileNotExistsException as e:
        messagebox.showerror("Error", f"The profile '{target_username}' does not exist.")
        console.print(str(e), style="red")
    except instaloader.exceptions.BadCredentialsException:
        messagebox.showerror("Error", "Invalid Instagram username or password.")
        console.print("Invalid Instagram username or password.", style="red")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred.")
        console.print(str(e), style="red")

else:
    # Restart the script
    messagebox.showinfo("Restart", "Restarting the script...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Close the popup window
root.destroy()

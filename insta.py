import sys
import getpass
import logging
import concurrent.futures
from colorama import Fore, Style
import instaloader
from pyfiglet import Figlet
from rich.console import Console
import tkinter as tk
from tkinter import messagebox

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def print_banner():
    f = Figlet(font="banner3-D")
    banner = f.renderText("Insta-Scraper")
    console.print(banner, "By Mr-Zanzibar, don.zanzibar (on discord)", style="bold green")

def prompt_credentials():
    console.print("Enter your Instagram username:", style="blue", end=" ")
    username = input()
    console.print("Enter your Instagram password:", style="blue", end=" ")
    password = getpass.getpass()
    return username, password

def handle_error(message):
    messagebox.showerror("Error", message)
    console.print(message, style="red")

def authenticate():
    username, password = prompt_credentials()
    return username, password

def download_profile(target_username):
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

        # download stories if available
        if profile.has_public_story:
            loader.download_stories([target_username], filename_target="{target}_{date}_" + instaloader.InstaloaderStoryItem.basefilename)

        # get number of followers
        followers_count = profile.followers
        console.print(f"Followers: {followers_count}")

    except instaloader.exceptions.ProfileNotExistsException as e:
        handle_error(f"The profile '{target_username}' does not exist. Error: {str(e)}")
    except instaloader.exceptions.BadCredentialsException:
        handle_error("Invalid Instagram username or password.")
    except Exception as e:
        handle_error(f"An error occurred: {str(e)}")

def start_download(target_username):
    result = messagebox.askquestion("Confirmation", f"Is '{target_username}' the correct target username?\nDo you want to download all the photos?")
    if result == 'yes':
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(download_profile, target_username)
    else:
        # Restart the script
        messagebox.showinfo("Restart", "Restarting the script...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    # Create a rich console
    console = Console()

    # Print the title and an introduction
    print_banner()

    # create an instance of Instaloader
    loader = instaloader.Instaloader()

    # check if the target_username is provided as a command-line argument
    if len(sys.argv) > 1:
        target_username = sys.argv[1]
    else:
        target_username = input(Fore.WHITE + "Enter the " + Fore.RED + "target" + Fore.WHITE + " profile username: " + Style.RESET_ALL)

    # prompt the user to enter the Instagram credentials
    username, password = authenticate()

    # Create a popup window
    root = tk.Tk()
    root.withdraw()

    # Show a message box with the target username
    start_download(target_username)

    # Close the popup window
    root.destroy()

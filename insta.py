import sys
import instaloader

# create an instance of Instaloader
loader = instaloader.Instaloader()

# enter your Instagram username and password
username = ""
password = ""

try:
    # login to Instagram
    loader.login(username, password)

    # check if the target_username is provided as a command-line argument
    if len(sys.argv) > 1:
        target_username = sys.argv[1]
    else:
        target_username = input("Enter the target profile username: ")

    # download the profile
    loader.download_profile(target_username, profile_pic=True)

    # access the profile object
    profile = instaloader.Profile.from_username(loader.context, target_username)

    # download all the photos
    for post in profile.get_posts():
        if not post.is_video:
            loader.download_post(post, target=profile.username)

    print("Profile downloaded successfully.")

except instaloader.exceptions.ProfileNotExistsException:
    print(f"The profile '{target_username}' does not exist.")
except instaloader.exceptions.BadCredentialsException:
    print("Invalid Instagram username or password.")

import base64
import spotipy
import requests
from PIL import Image, ImageFont, ImageDraw
from colorthief import ColorThief


#Spotify OAuth Token
token = str(input("Please enter your spotify oauth token: "))
sp = spotipy.Spotify(auth=token, requests_timeout=30)
sp.scope = ('ugc-image-upload')

def upload_random_covers():
    i = 1
    j = 1
    f = open('playlists.txt', 'r')
    for line in f:
        line = line[17:]
        line = line.replace('\n', '')
        playlist_info = sp.playlist(line)
        playlist_name = playlist_info['name']
        print(playlist_name + "\t successfully updated...")
        get_random_images()
        dom_color = calc_color("./images/random_img.jpg")
        edit_picture("./images/random_img.jpg", playlist_name, i, dom_color)
        while j<=i:
            path = "./images/post_img" +str(j)+ ".jpg"
            #print(path)
            with open(path, "rb") as enc_img:
                enc_txt = base64.b64encode(enc_img.read())
                sp.playlist_upload_cover_image(line, enc_txt)
            j = j+1
        i = i + 1

    #print("b64encoded: ", enc_txt)

### HELPER FUNCTION ###
def get_random_images():
    image_url = "https://random.imagecdn.app/600/600"
    img_data = requests.get(image_url).content
    path = "images/random_img.jpg"
    with open(path, 'wb') as handler:
        handler.write(img_data)

def get_playlists():
    f = open('playlists.txt', 'a+')
    f.truncate(0)
    playlists = sp.current_user_playlists()
    user = sp.current_user()
    username = user['display_name']
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if(playlist['owner']['display_name'] == username):
                playlist_info = (playlist['uri'] + "\n")
                #print(playlist_info)
                f.write(str(playlist_info))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    f.close()


### HELPER FUNCTION ###
def edit_picture(img, playlist_name, i, dom_color):
    pre_image = Image.open(img)
    font2 = ImageFont.truetype('./fonts/Montserrat-SemiBold', 50)
    image_editable = ImageDraw.Draw(pre_image)
    dommco = calc_dominant_color(img)
    outline_color = (59,59,59)

    image_editable.text((10,250), "This is", dom_color , font=font2)
    whitespaces = [k for k,j in enumerate(playlist_name) if (j==' ')]
    x = 10
    y = 300
    if(len(playlist_name) <= 20):
        image_editable.text((x-3,y-3), playlist_name, dom_color, font=font2)
        image_editable.text((x,y), playlist_name, dommco, font=font2)
    elif (len(playlist_name) < 40 and len(playlist_name) > 20):
        if(playlist_name[19] == ''):
            image_editable.text((x-3,y-3), playlist_name[:20], dom_color, font=font2)
            image_editable.text((x-3,y-3+50), playlist_name[21:], dom_color, font=font2)
            image_editable.text((x,y), playlist_name[:20], dommco, font=font2)
            image_editable.text((x,y+50), playlist_name[21:], dommco, font=font2)
        else: 
            for c in whitespaces:
                if (c < 20):
                    idx = c
            image_editable.text((x-3,y-3), playlist_name[:idx], dom_color, font=font2)
            image_editable.text((x-3,y-3+50), playlist_name[idx+1:idx+20], dom_color, font=font2)
            image_editable.text((x,y), playlist_name[:idx], dommco, font=font2)
            image_editable.text((x,y+50), playlist_name[idx+1:idx+20], dommco, font=font2)

    else:
        for c in whitespaces:
            if (c < 20):
                idx = c
        image_editable.text((x-3,y-3), playlist_name[:idx], dom_color, font=font2)
        image_editable.text((x,y), playlist_name[:idx], dommco, font=font2)
        for c in whitespaces:
            if (c < 40):
                idx2 = c
        image_editable.text((x-3,y-3+50), playlist_name[idx+1:idx2], dom_color, font=font2)
        image_editable.text((x-3,y-3+100), playlist_name[idx2+1:idx2+20], dom_color, font=font2)
        image_editable.text((x,y+50), playlist_name[idx+1:idx2], dommco, font=font2)
        image_editable.text((x,y+100), playlist_name[idx2+1:idx2+20], dommco, font=font2)

    output = "images/post_img"+ str(i) + ".jpg"
    pre_image.save(str(output))

### HELPER FUNCTION ###
def calc_color(path):
    color_thief = ColorThief(str(path))
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    #print("dominant color = ", dominant_color)
    inversed_color = str(255-dominant_color[0])+ ", " +str(255-dominant_color[1]) + ", " + str(255-dominant_color[2])
    tuple_color = tuple(map(int, inversed_color.split(', ')))
    #print(tuple_color, type(dominant_color), type(tuple_color))
    return tuple_color

### HELPER FUNCTION ###
def calc_dominant_color(path):
    color_thief = ColorThief(str(path))
    # build a color palette
    palette = color_thief.get_palette(color_count=8)
    return palette[6]
   


get_playlists()
upload_random_covers()


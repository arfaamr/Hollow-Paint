#Arfaa Rashid
#HKPaint_ArfaaRashid.py
#Hollow Knight themed paint project that allows user to use common paint features and tools like pencil, eraser, load, save, undo/redo, zoom, and various other extra features. 

from pygame import*
from pygame import Color as py_col
from random import*
from math import*
from tkinter import*
from tkinter import filedialog

root = Tk()
root.withdraw()

screen = display.set_mode((1024,760))

#-------------------------------------
###defaults

tool = "pencil"         #tool variable name that is used in the code. Default tool is pencil
tool_name = "Pencil"    #tool name that is blitted and shown in info box
tool_num = 0            #position at which all info about tool is in related lists
shortcut_name = "P"     #shortcut key used to choose tool
size = 5                #size of tool when drawing on canvas. Default is 5
 
effect_num = 0          #numbers on keyboard can be used to apply effect. if no key is pressed, effect num is 0
effect_key = K_0

l_col = (0,0,0)         #left click drawing colour. Default is black
r_col = (255,255,255)   #right click drawing colour. Default is white

click = False           #True when mousebuttondown, reset to False each loop. Allows rects that would otherwise be in MOUSEBUTTONUP so they are only selected once when clicked to be with the rest of the code

bGround = True          #toggles background image visibility
bGround_counter = 0     #used to index list of backgrounds
bGrounds = ["bground1.png","bground2.png","bground3.png","bground4.png","bground5.png",
            "bground6.png","bground7.jpg","bground8.jpg","bground9.jpg"] #list of backgrounds

playing = True          #toggles music on/off
music_counter = 0       #used to index list of music
music_list = ["greenpath.mp3","dirtmouth.mp3","mantis_lords.mp3","resting_grounds.mp3","soul_sanctum.mp3","city_of_tears.mp3"] #list of songs

box_time = 0            #used to alternate between the two types of info shown in the infobox
misc_tip_counter = -1   #used to index miscellaneous tip list.Counter increases before text blitted, so it will be at zero when text blits for the first time
misc_tip = False        #ensures only one tip is shown each cycle
info = True             #toggles infobox visibility

undo_list = []          #list will hold screencaps taken when mousebutton is released to undo what was drawn on the canvas
redo_list = []          #list will hold screencaps that were undone to redo what was drawn on the canvas

zoom = False            
cap_scale = (814,550)   #size of canvas. Size that screencaps of canvas are scaled to

perfect = False         #if perfect, shape tools will draw horizontal/vertical lines, squares, and circles depending on tool

fill_points = []        #points that need to be filled (are the right colour and are adjacent to another filled point) are added

stamp_list = ["knight.png","hornet.png","cornifer.png","quirrel.png","zote.png","sheo.png",
              "stag.png","grub.png","grimm.png","pale_king.png","charm_waywardcompass.png",
              "charm_souleater.png","charm_voidheart.png","charm_kingsoul.png","charm_grimmchild.png"]
stamp_counter = 0

polygon_points = []     #vertices of polygon are added


drawing = True          #needed because when you press the zoom_Rect, you collide with the zoomed canvas and it draws on the canvas. it will be False for that amount of time so nothing is drawn

grd_start_x = grd_start_y = grd_end_x = grd_end_y = grd_change_x = grd_change_y = grd_x = grd_y = 0 #default values/settings for gradient tool
hue = 0
hue_change = 5
left_click = False
right_click = False

#-------------------------------------
###Surfaces

canvas = Surface((814,550))     #Creates surface that can be copied.
canvas.fill((255,255,255))     
undo_list.append(canvas.copy()) #undo_list starts off with blank screen so this is the farthest back it can undo

info_surf = Surface((160,135))  #needs surface so it can be blitted above canvas when zoomed, because they overlap

hlight_surf = Surface((100,100),SRCALPHA) 

black_surf = Surface((814,550),SRCALPHA)    #Surfaces used for effects
red_surf = Surface((814,550),SRCALPHA)
green_surf = Surface((814,550),SRCALPHA)
blue_surf = Surface((814,550),SRCALPHA)
white_surf = Surface((814,550),SRCALPHA)
black_surf.fill((0,0,0,50))
red_surf.fill((255,0,0,50))
green_surf.fill((0,255,0,50))
blue_surf.fill((0,0,255,50))
white_surf.fill((255,255,255,50))


#------------------------------------------------
###Rects

cw_Rect = Rect(19,19,132,132)    #colour select rect
bw_Rect = Rect(164,19,22,162)    #black/white rect

canvas_Rect = Rect(200,10,814,550)

#tool_Rects  used to select tools
pencil_Rect = Rect(20,200,40,40)
eraser_Rect = Rect(80,200,40,40)
fill_Rect = Rect(140,200,40,40)
pbrush_Rect = Rect(20,260,40,40)
spray_Rect = Rect(80,260,40,40)
hlight_Rect = Rect(140,260,40,40)
line_Rect = Rect(20,320,40,40)
u_rectangle_Rect = Rect(80,320,40,40)
u_ellipse_Rect = Rect(140,320,40,40)
poly_Rect = Rect(20,380,40,40)
f_rectangle_Rect = Rect(80,380,40,40)
f_ellipse_Rect = Rect(140,380,40,40)
colpick_Rect = Rect(20,440,40,40)
gradient_Rect = Rect(80,440,40,40)
colmix_Rect = Rect(140,440,40,40)
stamp_Rect = Rect(665,660,90,90)

tool_Rects = [pencil_Rect,eraser_Rect,fill_Rect,pbrush_Rect,spray_Rect,hlight_Rect
             ,line_Rect,u_rectangle_Rect,u_ellipse_Rect,poly_Rect,f_rectangle_Rect,f_ellipse_Rect
             ,colpick_Rect,gradient_Rect,colmix_Rect,stamp_Rect]

#other buttons  used to access other features
clear_Rect = Rect(944,575,65,30)
undo_Rect = Rect(869,575,30,30)
redo_Rect = Rect(904,575,30,30)
zoom_Rect = Rect(795,575,65,30)
exitZoom_Rect = Rect(3,3,30,30)
switch_Rect = Rect(145,720,30,15)
bGround_Rect = Rect(979,620,30,30)
music_Rect = Rect(979,665,30,30)
down_Rect = Rect(643,560,30,60)
up_Rect = Rect(742,560,30,60)
save_Rect = Rect(205,575,30,30)
load_Rect = Rect(245,575,30,30)

#effect_Rects  used to apply effects
pixelate_Rect = Rect(245,620,80,45)
sepia_Rect = Rect(340,620,80,45)
grayscale_Rect = Rect(435,620,80,45)
black_Rect = Rect(530,620,80,45)
red_Rect = Rect(245,680,80,45)
green_Rect = Rect(340,680,80,45) 
blue_Rect = Rect(435,680,80,45) 
white_Rect = Rect(530,680,80,45) 

effect_Rects = [pixelate_Rect,sepia_Rect,grayscale_Rect,black_Rect,red_Rect,green_Rect,blue_Rect,white_Rect]


#-------------------------------------
###functions

#function for loading images
def image_load(surf,fname,scale,pos): #requires surface, filename and path of image, size it should be scaled to, and position it will be blitted at
    img = image.load(fname)
    img = transform.scale(img,scale)
    surf.blit(img,pos)


#function for rendering and blitting text
def text_fnt(surf,fType,txt,pos,box_size): #requires fonttype, the text being blitted, position it will be blitted at, and the space it must fit into
    txt_rend = fType.render(txt,True,(255,255,255))
    if txt_rend.get_width() > box_size:   #If text too long to fit
        words = []
        txt += " " #adds space at end of text so last word can also be sliced
        ##Puts each word in a list by slicing and appending
        for i in range(txt.count(" ")): 
            sp = txt.find(" ")
            words.append(txt[:sp+1])
            txt = txt[sp+1:]
        ##Decides which words will be in the same line
        list_pos = 0
        while True:
            word1_rend = fType.render(words[list_pos],True,(255,255,255))
            word2_rend = fType.render(words[list_pos+1],True,(255,255,255))
            if word1_rend.get_width() + word2_rend.get_width() < box_size:  #If the width of two words side by side fits in box,
                words[list_pos] += words[list_pos+1]                        # the words are put at the
                del words[list_pos+1]                                       # same list position
            else:
                list_pos += 1                                           #If the width exceeds the box size, it moves onto the next word
            if list_pos+1 >= len(words):                                # until it runs out of words
                break
        for j in range(len(words)):                                     #j is the number of lines
            line_rend = fType.render(words[j],True,(255,255,255))
            surf.blit(line_rend,(pos[0],pos[1]+j*20))
    else:
        surf.blit(txt_rend,(pos))


#function with all code that draws or blits onto the screen before the running loop, so it can be called again
def draw_fnt():
    screen.fill(0)

 #images
    if bGround == True:
        image_load(screen,("background_imgs/"+bGrounds[bGround_counter]),(1024,760),(0,0)) #background
    image_load(screen,("layout_imgs/c_sq.jpg"),(130,130),(20,20)) #colour select
    image_load(screen,("layout_imgs/b_w-strip.jpg"),(20,160),(165,20)) #black/white select
    image_load(screen,("layout_imgs/HK_paint.png"),(190,125),(785,610)) #Title
    image_load(screen,("layout_imgs/hk_logo.png"),(195,40),(0,555)) #various hollow knight images to make
    image_load(screen,("layout_imgs/elev.png"),(115,200),(650,560)) # the screen look nicer
    image_load(screen,("layout_imgs/down_off.png"),(30,60),(643,560)) 
    image_load(screen,("layout_imgs/up_off.png"),(30,60),(742,560)) 
    image_load(screen,("layout_imgs/dreamers.png"),(160,60),(20,490)) 
    image_load(screen,("layout_imgs/old_nail.png"),(150,28),(300,573))
    image_load(screen,("layout_imgs/pure_nail.png"),(150,28),(475,573))


#tool/effect/other feature images
    image_load(screen,("tool_imgs/pencil.png"),(32,30),(24,206))
    image_load(screen,("tool_imgs/eraser.png"),(36,32),(82,206))
    image_load(screen,("tool_imgs/bucket.png"),(25,30),(148,205))
    image_load(screen,("tool_imgs/paintbrush.png"),(30,38),(25,261))
    image_load(screen,("tool_imgs/spray.png"),(38,38),(81,261))
    image_load(screen,("tool_imgs/highlighter.png"),(36,36),(142,262))   
    image_load(screen,("tool_imgs/line.png"),(36,36),(22,322))
    image_load(screen,("tool_imgs/unfilledrect.png"),(36,36),(82,322))
    image_load(screen,("tool_imgs/unfilledellipse.png"),(36,36),(142,322))
    image_load(screen,("tool_imgs/polygon.png"),(34,32),(23,384))
    image_load(screen,("tool_imgs/filledrect.png"),(36,36),(82,382))
    image_load(screen,("tool_imgs/filledellipse.png"),(36,36),(142,382))
    image_load(screen,("tool_imgs/colourpicker.png"),(36,36),(22,442))
    image_load(screen,("tool_imgs/gradient.jfif"),(36,36),(82,442))
    image_load(screen,("tool_imgs/colourmixer.png"),(36,36),(142,442))

    image_load(screen,("tool_imgs/music.png"),(26,26),(981,667))
    image_load(screen,("tool_imgs/background.png"),(26,26),(981,622))
    image_load(screen,("tool_imgs/undo.png"),(26,26),(871,577))
    image_load(screen,("tool_imgs/redo.png"),(26,26),(906,577))
    image_load(screen,("tool_imgs/zoom.png"),(27,26),(817,577))
    image_load(screen,("tool_imgs/save.png"),(28,28),(206,576))
    image_load(screen,("tool_imgs/load.png"),(26,26),(247,577))

    image_load(screen,("tool_imgs/pixelate.jpg"),(70,35),(251,626))
    image_load(screen,("tool_imgs/sepia.jpg"),(70,35),(346,626))
    image_load(screen,("tool_imgs/grayscale.png"),(70,35),(441,626))
    image_load(screen,("tool_imgs/black.jpg"),(70,35),(536,626))
    image_load(screen,("tool_imgs/red.png"),(70,35),(251,686))
    image_load(screen,("tool_imgs/green.jpg"),(70,35),(346,686))
    image_load(screen,("tool_imgs/blue.jpg"),(70,35),(441,686))
    image_load(screen,("tool_imgs/white.jpg"),(70,35),(536,686))


 #Drawing Rects
    draw.rect(screen,(255,255,255),cw_Rect,1) #colour select box
    draw.rect(screen,(255,255,255),bw_Rect,1) #b/w colour select box

    draw.rect(screen,(255,255,255),(19,159,22,22)) #rects showing selected
    draw.rect(screen,(255,255,255),(49,159,22,22)) # lCol and rCol

    if len(undo_list) > 0 and zoom == False:            #Only draw canvasRect the first time function is called(before runs)
        undo = transform.scale(undo_list[-1],cap_scale) # ,otherwise canvas will be wiped every time it's called
        canvas.blit(undo,(0,0))                         
    else:
        draw.rect(screen,(255,255,255),canvas_Rect)


#tool_Rects
    for toolrect in tool_Rects:     #draws all tool select rects
        if toolrect != stamp_Rect:  # besides stamp, because it only exists so it can be collided with, not to be seen
            draw.rect(screen,(255,255,255),toolrect,2)


#other feature Rects
    draw.rect(screen,(255,255,255),clear_Rect,2)
    draw.rect(screen,(255,255,255),undo_Rect,2)
    draw.rect(screen,(255,255,255),redo_Rect,2)
    draw.rect(screen,(255,255,255),zoom_Rect,2)
    draw.rect(screen,(255,255,255),bGround_Rect,2)
    draw.rect(screen,(255,255,255),music_Rect,2)
    draw.rect(screen,(255,255,255),save_Rect,2)
    draw.rect(screen,(255,255,255),load_Rect,2)


#effect_Rects
    for effectrect in effect_Rects:
        draw.rect(screen,(255,255,255),effectrect,2)
draw_fnt()

#function for playing and pausing music files
def play_music():
    global music_counter
    init()
    if playing == False:
        mixer.music.stop()
    else:
        mixer.music.load("music/"+music_list[music_counter])
        mixer.music.play()
play_music()

#------------------------------------------------
###font

font.init()
fType_italics = font.SysFont("Times New Roman", 20)
fType_italics.set_italic(True)    
fType = font.SysFont("Times New Roman", 20)
fType_small = font.SysFont("Times New Roman", 15)

#------------------------------------------------
###lists

#variable names used in code
tools = ["pencil","eraser","fill","pbrush","spray","hlight"
         ,"line","u_rect","u_ellipse","polygon","f_rect","f_ellipse"
         ,"colpick","gradient","colmix","stamp"]

#tool names blitted in infobox
tool_names = ["Pencil","Eraser","Fill Bucket","Paint Brush","Spray Paint","Highlighter"
             ,"Line","Rectangle","Ellipse","Polygon","Rectangle","Ellipse"
             ,"Colour Picker","Gradient","Colour Mixer","Stamps"]

#info and tip for each tool, blitted in infobox
tool_tips = ["Ordinary pencil.","Pretend it never happened.","For the lazy."
            ,"A paint brush that never dries.","Vandalism is bad though.","Start taking class notes on HK Paint!"
            ,"Hold shift for a perfect line.","Unfilled. Hold shift for a square.","Unfilled. Hold shift for a circle."
            ,"Left-click to place points, right-click to close.","Filled. Hold shift for a square.","Filled. Hold shift for a circle."
            ,"Click on a colour on the canvas to draw with.","The direction you slide your mouse affects it.","Blends colours on canvas."
            ,"Drag Hollow Knight NPCs onto the canvas!"]

#keycodes used to index the list that shows which keys are pressed
shortcut_keys = [K_p,K_e,K_f,K_b,K_s,K_h,K_l,K_r,K_c,K_g,K_w,K_v,K_k,K_d,K_m,K_a]

#shortcuts used to access tool, blitted in infobox
shortcut_names = ["P","E","F","B","S","H","L","R","C","G","W","V","K","D","M","A"]

#shortcut keycodes for effects
effect_keys = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8]

#miscellaneous tips to explain things to user that may not be obvious
misc_tips = ["Left-click to change the background image.", "Right-click to toggle background on/off.","Hold control and press the arrow keys to change size faster."
             ,"Left-click to change the music.","Right-click to mute/unmute the music.","You can apply the same effect multiple times to increase the effect."
             ,"Tools can also be accessed with shortcut keys.","You can change stickers with arrow keys."]

#------------------------------------------------

running = True
while running:
    
    click = False
    
    for e in event.get():
        if e.type == QUIT:
            running = False
            
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1 or e.button == 3:
                click = True

                if canvas_Rect.collidepoint(mx,my):
                    start_x,start_y = grd_start_x,grd_start_y = nmx,nmy     #Start pos for shapes / gradient

                    if tool == "fill":
                        orig_col = pick_col         #colour at position where mousebuttondown is the colour that will be filled
                        fill_points.append((nmx,nmy))

        if e.type == MOUSEBUTTONUP:

            if tool == "polygon" and canvas_Rect.collidepoint(mx,my):
                if e.button == 1:       #if left-click, vertices of polygon are added to list
                    polygon_points.append((nmx,nmy))
                elif e.button == 3:     #if right-click, polygon closes and list is emptied
                    polygon_points = []

            if tool == "gradient" and (e.button == 1 or e.button == 3): 
                    grd_end_x,grd_end_y = nmx,nmy   #gradient start and end points determine which direction to draw the gradient


            #undo/redo
            ##when something is drawn on the canvas, a copy of the surface is added to the undo list
            ##when the undo_Rect is pressed, the last copy is deleted because that's the current screen, and the new last copy is blitted and addecd to the redo_List and deleted from the undo_List
            ##when the redo_Rect is pressed, it blits the last copy and returns it to the undo_List and deletes it
            if e.button == 1 or e.button == 3: #If right-click or left-click
                if tool!='colpick' and canvas_Rect.collidepoint(mx,my):
                    undo_list.append(canvas.copy())

                    if canvas_Rect.collidepoint(mx,my) and drawing == True:
                        redo_list = []   #If you draw again, can no longer redo

                if undo_Rect.collidepoint(mx,my) and zoom == False:
                    if len(undo_list) > 1:
                        redo_list.append(undo_list[-1])
                        del undo_list[-1]
                        undo = transform.scale(undo_list[-1],cap_scale)
                        canvas.blit(undo,(0,0))

                if redo_Rect.collidepoint(mx,my) and zoom == False:
                    if len(redo_list) > 0:
                        redo = transform.scale(redo_list[-1],cap_scale)
                        canvas.blit(redo,(0,0))
                        undo_list.append(redo_list[-1])
                        del redo_list[-1]
        
        if e.type == KEYDOWN:
            
            #change tool size
            if key.get_pressed()[K_LCTRL] or key.get_pressed()[K_RCTRL] == 1: #if control key is pressed, changes by 5
                if e.key == K_RIGHT: #change size with left/right arrow keys
                    size += 5
                elif e.key == K_LEFT:
                    size -= 5
            else:
                if e.key == K_RIGHT: #if control not pressed, changes by 1
                    size += 1
                elif e.key == K_LEFT:
                    size -= 1
            if size > 100: #max size is 100
                size = 100
            if size < 1: #min size is 1
                size = 1

            #change stamp image using arrow keys
            if e.key == K_UP:
                if stamp_counter+1 >= len(stamp_list):
                    stamp_counter = 0
                else:
                    stamp_counter += 1
                draw_fnt()
            elif e.key == K_DOWN:
                if stamp_counter-1 < 0:
                    stamp_counter = len(stamp_list) - 1
                else:
                    stamp_counter -= 1
                draw_fnt()

                
            #Keyboard shortcuts to switch tools
            for key_code in shortcut_keys:
                if key.get_pressed()[key_code] == 1:
                    tool_num = shortcut_keys.index(key_code)    #finds index position of shortcut key pressed
                    tool = tools[tool_num]                      #all lists are related at indices,
                    tool_name = tool_names[tool_num]            # so this finds all corresponding info
                    shortcut_name = shortcut_names[tool_num]

            #Keyboard shortcuts to apply effects
            for effect_key in effect_keys:                      #finds index position of effect_key pressed and sets effect_num equal to
                if key.get_pressed()[effect_key] == 1:          # corresponding number for effect
                    effect_num = effect_keys.index(effect_key) +1
                    
#------------------------------------------------

    mb = mouse.get_pressed()           

    mx,my = mouse.get_pos()         #Because canvas is a Surface being blitted at 200,10 or 3,36, everything drawn on canvas is moved 
    if zoom == False:               # -200,-10 or -3,-36. In order for drawing to appear where the mouse is after being blitted,
        nmx,nmy = mx-200,my-10      # it must draw at mx-200,my-10 or mx-3,my-36. nmx,nmy -> new mousepos       
    else:
        nmx,nmy = mx-3,my-36       


    if canvas_Rect.collidepoint(mx,my):         #if picking colour from canvas, since it's moved it must pick at nmx,nmy
        pick_col = canvas.get_at((nmx,nmy))     #if picking from the colour select images, the mouse isn't over the canvas
    else:                                       # and doesn't need to be moved
        pick_col = screen.get_at((mx,my))    


    if zoom:                    #Size of canvas for scaling screen_captures depends on whether zoom is true or false              
        cap_scale = (1018,688)  # , because the size of canvas changes
    else:
        cap_scale = (814,550)


    #Draws a horizontal/vertical line, square, or circle depending on tool
    if key.get_pressed()[K_LSHIFT] or key.get_pressed()[K_RSHIFT] == 1: #If shift is held, shape drawn 'perfectly'
        perfect = True
    else:
        perfect = False


    if mb[0] == 1:  #A different colour can be selected with left(l_col) and right_r_col) mousebuttons
        col = l_col # col is the drawing colour. Depending on which mb is pressed, it will be l_col or r_col
    elif mb[2] == 1:
        col = r_col



#effects
    #canvas becomes pixelated by taking the average colour of a range and drawing a square of that size and colour
    if (pixelate_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 1:
        for pix_x in range(0,cap_scale[0],11):       
            for pix_y in range(0,cap_scale[1],11):
                pix_avg_col = transform.average_color(canvas,(pix_x,pix_y,11,11))
                draw.rect(canvas,pix_avg_col,(pix_x,pix_y,11,11))
        undo_list.append(canvas.copy())
        effect_num = 0

    #applies sepia effect to canvas by getting colour at each position and multiplying it by the numbers that result in sepia colour
    if (sepia_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 2:
        for sep_x in range(cap_scale[0]):        #loops for each pixel on the screen
            for sep_y in range(cap_scale[1]):    # number of pixels on the screen differs depending on whether zoomed or not
                sep_r,sep_g,sep_b,sep_a = canvas.get_at((sep_x,sep_y))

                sep_r2 = min(255,int(sep_r* 0.393 + sep_g* 0.769 + sep_b* 0.189)) #creates colour code that
                sep_g2 = min(255,int(sep_r* 0.349 + sep_g* 0.686 + sep_b* 0.168)) #  results in sepia effect
                sep_b2 = min(255,int(sep_r* 0.272 + sep_g* 0.534 + sep_b* 0.131))

                canvas.set_at((sep_x,sep_y),(sep_r2,sep_g2,sep_b2))
        undo_list.append(canvas.copy())
        effect_num = 0

    #grayscale effect is applied by getting colour at each position on the screen, and making its RGB equal to the average of its RGB values
    if (grayscale_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 3:

        for gs_x in range(cap_scale[0]):
            for gs_y in range(cap_scale[1]):
                gs_r,gs_g,gs_b,gs_a = canvas.get_at((gs_x,gs_y))
                if gs_r != gs_g and gs_g != gs_b and gs_b != gs_r:  #if they're already equal, skips them.
                                                                            # saves time because often a lot of the canvas is white or black
                    gs_r2 = (gs_r+gs_g+gs_b)//3
                    gs_g2 = gs_b2 = gs_r2           #r,g,b must be equal to make gray

                    canvas.set_at((gs_x,gs_y),(gs_r2,gs_g2,gs_b2))
        undo_list.append(canvas.copy())
        effect_num = 0

    #canvas appears darker by blitting a partially transparent black surface over canvas
    if (black_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 4:
        black_scaled = transform.scale(black_surf,(cap_scale))
        canvas.blit(black_scaled,(0,0))
        undo_list.append(canvas.copy())
        effect_num = 0

    #canvas appears more red by blitting a partially transparent red surface over canvas
    if (red_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 5:
        red_scaled = transform.scale(red_surf,(cap_scale))
        canvas.blit(red_scaled,(0,0))
        undo_list.append(canvas.copy())
        effect_num = 0

    #canvas appears more green by blitting a partially transparent green surface over canvas
    if (green_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 6:
        green_scaled = transform.scale(green_surf,(cap_scale))
        canvas.blit(green_scaled,(0,0))
        undo_list.append(canvas.copy())
        effect_num = 0

    #canvas appears more blue by blitting a partially transparent blue surface over canvas
    if (blue_Rect.collidepoint(mx,my) and click and zoom == False)or effect_num == 7:
        blue_scaled = transform.scale(blue_surf,(cap_scale))
        canvas.blit(blue_scaled,(0,0))
        undo_list.append(canvas.copy())
        effect_num = 0

    #canvas appears lighter by blitting a partially transparent white surface over canvas
    if (white_Rect.collidepoint(mx,my) and click and zoom == False) or effect_num == 8:
        white_scaled = transform.scale(white_surf,(cap_scale))
        canvas.blit(white_scaled,(0,0))
        undo_list.append(canvas.copy())
        effect_num = 0




    if zoom == False: #if zoom, canvas covers these options/features

        draw.rect(screen,l_col,(20,160,20,20)) #rects show selected left and right colour
        draw.rect(screen,r_col,(50,160,20,20))



#tool select
        if click:
            for i in range(16):                         #There are 16 tools. In all lists, they are listed in the same order
                if tool_Rects[i].collidepoint(mx,my):   # ,so the information at i in all lists refers to the same tool.
                    tool = tools[i]                     #Variable name for tool that is used in the code
                    tool_name = tool_names[i]           #Name displayed in the infobox
                    tool_num = i                        #Used to find the corresponding toolTip text
                    shortcut_name = shortcut_names[i]   #Keyboard shortcut to choose tool


    
#other features
        if clear_Rect.collidepoint(mx,my) and mb[0] == 1:
            canvas.fill((255,255,255))
            undo_list.append(canvas.copy())

        if bGround_Rect.collidepoint(mx,my) and click: 
            if mb[0] == 1:                              #Switch background images
                if bGround_counter+1 >= len(bGrounds):  #If last background in list, restart at first image
                    bGround_counter = 0
                else:
                    bGround_counter +=1
                draw_fnt()                              #calls function to draw new background and redraw everything else overtop 
            elif mb[2] == 1: #Toggles background picture on/off
                if bGround == True:
                    bGround = False
                else:
                    bGround = True
                draw_fnt()

        if music_Rect.collidepoint(mx,my) and click: 
            if mb[0] == 1:                              #Switch background music
                if music_counter+1 >= len(music_list):  #If last song in list, restart at first song
                    music_counter = 0
                else:
                    music_counter +=1
                play_music()

            elif mb[2] == 1: #Toggles music on/off
                if playing == True:
                    playing = False
                else:
                    playing = True
                play_music()

        if mixer.music.get_busy() == 0 and playing == True: #If song finishes, play next 
            if music_counter+1 >= len(music_list):          #If last song in list, restart at first song
                music_counter = 0
            else:
                music_counter +=1
            play_music()


        #Clicking up/down images changes stamp. 
        if down_Rect.collidepoint(mx,my):   #If image is being collided with, blits lit up button
            image_load(screen,"layout_imgs/down_on.png",(30,60),(643,560))
            if click:
                if stamp_counter-1 < 0:     #If last stamp at list, restarts at first
                    stamp_counter = len(stamp_list) - 1
                else:
                    stamp_counter -= 1
                draw_fnt()
        else:
            image_load(screen,"layout_imgs/down_off.png",(30,60),(643,560))        

        if up_Rect.collidepoint(mx,my):
            image_load(screen,"layout_imgs/up_on.png",(30,60),(742,560))
            if click:
                if stamp_counter+1 >= len(stamp_list):
                    stamp_counter = 0
                else:
                    stamp_counter += 1
                draw_fnt()
        else:
            image_load(screen,"layout_imgs/up_off.png",(30,60),(742,560))

        image_load(screen,"stamp_imgs/"+stamp_list[stamp_counter],(90,90),(665,660))


        #Save and Load open tkinter dialogue boxes
        if save_Rect.collidepoint(mx,my) and click:
            result = filedialog.asksaveasfilename()
            if result is not "":
                image.save(canvas,result+".png") #saves canvas as filename that was entered
        elif load_Rect.collidepoint(mx,my) and click:
            result = filedialog.askopenfilename(filetypes = [("Picture files", "*.png;*.jpg")])
            if result is not "":
                image_load(canvas,result,cap_scale,(0,0)) #loads selected image from filepath selected
                undo_list.append(canvas.copy())


        #Enlarges canvas and removes most features from screen
        if zoom_Rect.collidepoint(mx,my) and mb[0] == 1: 
            zoom = True
            drawing = False             #False so canvas isn't drawn on while zooming
            zoom_cap = canvas.copy()    #Copies what is drawn currently so it can be blitted again after everything is enlarged
            canvas = Surface((1018,688))#Canvas is approx 1.25x larger
            canvas_Rect = Rect(3,36,1018,688) 
            draw.rect(screen,(255,255,255),canvas_Rect)                                                              
            screen.fill(0)                             
            zoom_cap_scaled = transform.scale(zoom_cap,(1018,688)) #enlarges and blits what was drawn on canvas
            canvas.blit(zoom_cap_scaled,(0,0))                   
        
            del undo_list[-1]   #Counts as collision with canvas_Rect when zoom_Rect is clicked
                                # ,but nothing is actually drawn so it doesn't need to be added to the list
    else:
        drawing = True  #Done zooming, so can now draw again
        draw.rect(screen,(255,255,255),exitZoom_Rect,2)
        image_load(screen,("tool_imgs/zoom.png"),(27,26),(5,5))
        
        if exitZoom_Rect.collidepoint(mx,my) and mb[0] == 1:
            zoom_cap = canvas.copy()
            canvas = Surface((814,550))
            canvas_Rect = Rect(200,10,814,550)          #same as before, but in reverse(shinks canvas, moves back to
            draw.rect(screen,(255,255,255),canvas_Rect) # original position, and background/rects are drawn again          
            draw_fnt()                             
            zoom_cap_scaled = transform.scale(zoom_cap,(814,550))
            canvas.blit(zoom_cap_scaled,(0,0))
            zoom = False



#draw on canvas
    if canvas_Rect.collidepoint(mx,my) and (mb[0] == 1 or mb[2] == 1) and drawing == True:
        screen.set_clip(canvas_Rect)

        if tool == "pencil":
            dist = round(hypot(nmx-omx,nmy-omy)) #draws a circle at each position from old mousepos to current mousepos
            dist = max(dist,1)
            for i in range(dist):
                dx = round(i*(nmx-omx)/dist)
                dy = round(i*(nmy-omy)/dist)
                draw.circle(canvas,col,(omx+dx,omy+dy),size)

        if tool == "eraser":
            dist = round(hypot(nmx-omx,nmy-omy)) #draws a white square at each position from old mousepos to current mousepos
            dist = max(dist,1)
            for i in range(dist):
                dx = round(i*(nmx-omx)/dist)
                dy = round(i*(nmy-omy)/dist)
                draw.rect(canvas,(255,255,255),(omx+dx-size/2,omy+dy-size/2,size,size))

        if tool == "fill":
            while len(fill_points) > 0:
                for point in fill_points:    #Fills point and spreads out to adjacent points and fills if original colour
                    if canvas.get_at((point)) == orig_col:

                        draw.rect(canvas,col,(point[0],point[1],5,5))   #Goes by 5 pixels instead of 1 because otherwise the list has so many points that it crashes
                                                                        # ,even for a small fill area. This means there's sometimes an unfilled line at the edge of the area being filled.
                        left = (point[0]-5,point[1])                    #Finds 4 adjacent points
                        if canvas.get_at((left)) == orig_col and fill_points.count(left) == 0 and left > (0,0) and left < (814,550): #only adds if point isn't already in the list, and is inside the canvas
                            fill_points.append(left)
                        
                        right = (point[0]+5,point[1])
                        if canvas.get_at((right)) == orig_col and fill_points.count(right) == 0 and right > (0,0) and right < (814,550):
                            fill_points.append(right)
                            
                        up = (point[0],point[1]-5)
                        if canvas.get_at((up)) == orig_col and fill_points.count(up) == 0 and up > (0,0) and up < (814,550):
                            fill_points.append(up)
                            
                        down = (point[0],point[1]+5)
                        if canvas.get_at((down)) == orig_col and fill_points.count(down) == 0 and down > (0,0) and down < (814,550):
                            fill_points.append(down)

                        fill_points.remove(point)

        elif tool != "fill": #if fill is abandoned midway through, list is emptied so it doesn't affect next fill
            fill_points = []

        #Chooses random position in range around current mousepos and draws line to same position in range around old mousepos
        #Creates effect of individual bristles of paintbrush drawing on canvas
        if tool == "pbrush":
            for j in range(size):                   #Number of lines drawn is proportional to size
                randX = randint(-size,size)         #Chooses random position in range around mouse
                randY = randint(-size,size) 
                dist = round(hypot(nmx-omx,nmy-omy)) 
                dist = max(dist,1)
                for i in range(dist):
                    dx = round(i*(nmx-omx)/dist)    #Draws circle at every pos in dist to make it smoother
                    dy = round(i*(nmy-omy)/dist)
                    
                    draw.circle(canvas,col,(omx+dx+randX,omy+dy+randY),1) #randX,randY ensure that endpoints of line are same distance from old mousepos as startpoints from current mousepos

            
        if tool == "spray":
            for i in range(size//5):            #circles drawn per loop proportionate to size
                spray_x = randint(nmx-size,nmx+size)  #spX and spY are x and y coordinates used for spray can tool
                spray_y = randint(nmy-size,nmy+size)  #circles are drawn at random positions within range of mouse
                spray_dist = hypot(nmx-spray_x,nmy-spray_y)   #if outside a circular range around mouse, doesn't draw
                if spray_dist < size:
                    draw.circle(canvas,col,(spray_x,spray_y),randint(1,5))  #circles are drawn randomly sized


        if tool == "hlight":
            hlight_surf = Surface((100,100),SRCALPHA) #Blits partially transparent surface at each point between mousepos and old mousepos
            draw.rect(hlight_surf,(col[0],col[1],col[2],5),(size//2,size//2,size,size))
            dist = round(hypot(nmx-omx,nmy-omy)) 
            dist = max(dist,1)
            for i in range(dist):
                dx = round(i*(nmx-omx)/dist)
                dy = round(i*(nmy-omy)/dist)
                canvas.blit(hlight_surf,(omx+dx-size,omy+dy-size))

        
        if tool == "line":
            undo = transform.scale(undo_list[-1],(cap_scale))
            canvas.blit(undo,(0,0))

            end_x,end_y = nmx,nmy #end pos
            if perfect:
                hx,hy = nmx,start_y             #endpoints if line is horizontal
                vx,vy = start_x,nmy             #endpoints if line is vertical
                hDist = hypot(nmx-hx,nmy-hy)    #distance from mousepos to endpos if horizontal
                vDist = hypot(nmx-vx,nmy-vy)    #distance from mousepos to endpos if vertical
                if hDist < vDist:               #chooses whichever is closest
                    end_x,end_y = hx,hy
                else:
                    end_x,end_y = vx,vy
            draw.line(canvas,col,(start_x,start_y),(end_x,end_y),size)


        if tool == "u_rect" or tool == "f_rect":
            undo = transform.scale(undo_list[-1],(cap_scale))
            canvas.blit(undo,(0,0))
            
            rec = Rect(start_x,start_y,nmx-start_x,nmy-start_y)
              
            if perfect:             #sets width and height of rect equal
                                    # to the smaller of the two to make it a square
                if rec.w < 0:       #Absolute values are used so negatives don't affect which is smaller
                    neg_w = True    # and the negative are added on again afterwards
                else:
                    neg_w = False
                if rec.h < 0:
                    neg_h = True
                else:
                    neg_h = False
                
                rec.w = min(abs(rec.w),abs(rec.h))    
                rec.h = min(abs(rec.w),abs(rec.h))    

                if neg_w:
                    rec.w *= -1
                if neg_h:
                    rec.h *= -1

            rec.normalize() 
            
            if tool == "u_rect":
                draw.rect(canvas,col,rec,size)
            else:
                draw.rect(canvas,col,rec)


        if tool == "u_ellipse" or tool == "f_ellipse":
            undo = transform.scale(undo_list[-1],(cap_scale))
            canvas.blit(undo,(0,0))
            
            rec = Rect(start_x,start_y,nmx-start_x,nmy-start_y)
              
            if perfect:             #sets width and height of ellipse equal
                                    # to the smaller of the two to make it a circle
                if rec.w < 0:       #Absolute values are used so negatives don't affect which is smaller
                    neg_w = True    # and the negative are added on again afterwards
                else:
                    neg_w = False
                if rec.h < 0:
                    neg_h = True
                else:
                    neg_h = False
                
                rec.w = min(abs(rec.w),abs(rec.h))    
                rec.h = min(abs(rec.w),abs(rec.h))    

                if neg_w:
                    rec.w *= -1
                if neg_h:
                    rec.h *= -1

            rec.normalize()

            if tool == "u_ellipse":
                    if size > rec.w/2 or size > rec.h/2: #If size greater than radius, draw filled
                        draw.ellipse(canvas,col,rec)
                    else:
                        draw.ellipse(canvas,col,rec,size)
            else:
                draw.ellipse(canvas,col,rec)


        if tool == "polygon":    
            if mb[0] == 1:      #only draw points with left mb
                undo = transform.scale(undo_list[-1],(cap_scale))
                canvas.blit(undo,(0,0))

                draw.circle(canvas,col,(nmx,nmy),size)
            elif mb[2] == 1:     #right mb closes polygon
                draw.polygon(canvas,l_col,polygon_points,size)

    
        if tool == "colmix":
            for x in range(-size//2,size//2,5):     #finds average colour of square area around mouse and 
                for y in range(-size//2,size//2,5): #draws square of that colour
                    cx,cy = nmx+x,nmy+y
                    if canvas_Rect.collidepoint(mx+x,my+y):
                        avg_col = transform.average_color(canvas,(cx,cy,size//2,size//2))
                        draw.rect(canvas,avg_col,(cx,cy,size//2,size//2))


        if tool == "stamp":                         #Blits selected stamp at mouseposition
            undo = transform.scale(undo_list[-1],(cap_scale))
            canvas.blit(undo,(0,0))
            image_load(canvas,"stamp_imgs/"+stamp_list[stamp_counter],(size*5,size*5),(nmx-size*5//2,nmy-size*5//2))

            
        screen.set_clip(None)
        
    #Outside of drawing on canvas if statement because they have different requirements 
    if (tool == "colpick" and canvas_Rect.collidepoint(mx,my)) or zoom == False and (bw_Rect.collidepoint(mx,my) or cw_Rect.collidepoint(mx,my)):
        if mb[0] == 1:              #Depending on which mousebutton used, colour at the location is assigned to that variabale
            l_col = pick_col
        if mb[2] == 1:
            r_col = pick_col


    if tool == "gradient" and canvas_Rect.collidepoint(mx,my):
            if mb[0] == 1:              #finds out which mb is being used to draw gradient, and if it is released
                left_click = True       # ,resets numbers
                right_click = False
            elif mb[2] == 1:
                left_click = False
                right_click = True

            if mb[0] == 1 or mb[2] == 1:
                
                grd_change_x = grd_start_x - grd_end_x      #determines direction of gradient
                grd_change_y = grd_start_y - grd_end_y
                if grd_change_x < 0:
                    direction_x = "right"
                elif grd_change_x > 0:
                    direction_x = "left"
                if grd_change_y < 0:
                    direction_y = "down"
                elif grd_change_y > 0:
                    direction_y = "up"
                if abs(grd_change_x) > abs(grd_change_y):   #if mouse travels diagonally, chooses the direction
                    direction = direction_x                 # it traveled the farthest in
                elif abs(grd_change_x) < abs(grd_change_y):
                    direction = direction_y

                grd_col = py_col(0,0,0)         #can't directly set attributes of imported object, so must assign it to a variable first

                if col[0] == col[1] == col[2]:
                    col_type = "full"
                    min_hue = 0
                    max_hue = 360
                elif max(col[0],col[1],col[2]) == col[0]:   #gradient is diff colours based on selected colour
                    col_type = "red"                        #values for hue range from 0 to 360
                    min_hue = 240
                    max_hue = 360                           
                elif max(col[0],col[1],col[2]) == col[1]:
                    col_type = "green"
                    min_hue = 0
                    max_hue = 120
                elif max(col[0],col[1],col[2]) == col[2]:
                    col_type = "blue"
                    min_hue = 120
                    max_hue = 240
                
                hue += hue_change   
                if hue >= max_hue:                   
                    hue_change = -5
                elif hue <= min_hue:
                    hue_change = 5
                  
                grd_col.hsla = (hue,100,50)        #it's easier to create a gradient with hsla colour values than rgba because then you only need to change h instead of rgb
                
                if direction == "right":            #Draws rectangles of decreasing size while colour changes
                    if grd_x < 814:
                        grd_x += 11
                    draw.rect(canvas,grd_col,(grd_x,0,814-grd_x,550))

                elif direction == "left":
                    if grd_x < 814:
                        grd_x += 11
                    draw.rect(canvas,grd_col,(0,0,814-grd_x,550))

                elif direction == "up":
                    if grd_y < 550:
                        grd_y += 11
                    draw.rect(canvas,grd_col,(0,0,814,550-grd_y))

                elif direction == "down":
                    if grd_y < 550:
                        grd_y += 11
                    draw.rect(canvas,grd_col,(0,grd_y,814,550-grd_y))


            if left_click and mb[0] == 0:   #if the mousebutton being used to draw the 
                grd_x = 0                   # gradient is released, numbers are reset
                grd_y = 0
                left_click = False
            elif right_click and mb[2] == 0:
                grd_x = 0
                grd_y = 0
                right_click = False

            

    
    if zoom == False:       #canvas is blitted at different location depending on whether zoomed or not
        screen.blit(canvas,(200,10))
    else:
        screen.blit(canvas,(3,36))
            




#infoBox
    image_load(info_surf,("background_imgs/hk_boxcut3.png"),(160,135),(0,0)) #infobox background image
    draw.rect(info_surf,(255,255,255),(0,0,160,135),2)
        
#text
    if box_time//75%2 == 0: #alternates between different kinds of info
        text_fnt(info_surf,fType_italics,"Info:",(60,5),160) #Header text
        text_fnt(info_surf,fType,tool_name,(5,27),160) #Tool name text
        text_fnt(info_surf,fType,str(size),(127,27),160) #Tool size text
        text_fnt(info_surf,fType,tool_tips[tool_num],(5,47),160) #Tool tips
        text_fnt(info_surf,fType_small,str(mx),(3,115),160) #Mouse position(x)
        text_fnt(info_surf,fType_small,str(my),(40,115),160) #Mouse position(y)
        text_fnt(info_surf,fType_small,shortcut_name,(90,115),160) #Shortcut key to choose tool
        misc_tip = False
    else:
        if misc_tip == False: #if tip has not been shown yet
            if misc_tip_counter+1 >= len(misc_tips):
                misc_tTip_counter = 0
            else:
                misc_tip_counter += 1
            misc_tip = True #tip has been shown, won't show another or increase counter 

        text_fnt(info_surf,fType_italics,"Tips:",(60,5),160) #Header text
        text_fnt(info_surf,fType,misc_tips[misc_tip_counter],(5,27),160) #Miscellaneous tips

    if info == False:       #when visibility toggled off, surface is blitted transparent
        info_surf.set_alpha(0)
    else:
        info_surf.set_alpha(255)
    
    screen.blit(info_surf,(20,605)) 

    draw.rect(screen,(255,255,255),switch_Rect,2)
    if switch_Rect.collidepoint(mx,my) and click and mb[0] == 1: #switch between info in infobox at will
        if box_time//75%2 == 0:
            box_time = 75
        else:
            box_time = 0

    elif switch_Rect.collidepoint(mx,my) and click and mb[2] == 1: #Toggles infobox visibility
        if info == True:
            info = False
            draw_fnt()
        else:
            info = True
            
        

    omx,omy = nmx,nmy   #position that mouse was at last loop. omx,omy -> old mousepos
    box_time += 1
    
    display.flip()
quit()





'''
gradient nums change if zoom ***


move set clip(None) to after colpicker?

unfilled ellipse is wack


miscCounter increasing is stupid

if for 1st click, start off canvas and click canvas, no smx/smy

program runs slow - bc of printstatements? removed but still slow

fix sm/em ???whats that >start and end mouse pos


###have grayed out undo/redo pic if list empty - if time. i have time

cursor - (draw a crosshair at mx,my, like paint. dist inc with tool size)
    - set mouse visibility. crosshair dep on tool - if time. i have time. i dont but i want to have time

'''

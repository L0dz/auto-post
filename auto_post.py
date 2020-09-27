import os
import json
from datetime import datetime
import time
from __posting__ import upload, upload_vid
from getpass import getpass
username=''
password=''
posts = []
info=''

class post:
    def __init__(self, desc, date,img_path, title):
        self.title = title
        self.description = desc
        self.date = date
        self.path = img_path

def go_back(string):
    if(string == '$'):
        return True
    else:
        return False

def save():
    #save data
    data=dict()
    # data = frozenset(data.items())
    for p in posts:
        print(f'Title: {p.title}')
        data[p.title]={
            'title':p.title,
            'description':p.description,
            'path':p.path,
            'date':str(p.date[0]) + "/" + str(p.date[1]) + "/" + str(p.date[2]) + " " + str(p.date[3])+":" + str(p.date[4])
        }
        
    with open('posts_list.json', 'w') as f:
        json.dump(data, f, indent=2)

def fix_date(date):
    #vars
    word=''
    _date=''
    newdate = []
    count=0
    print(f'Date recived: "{date}"')
    #remove / and : and create a list
    try:
        for char in date:
            if char == '/' or char == ':':
                word=' '
                count+=1
            else:
                word = char
            _date+=word

        newdate = _date.split()
    except Exception as e:
        print('Error: Date not valid, ' + str(e))
        inputs()

    #print(newdate)

    #validate the date
    if(count!=3 or len(newdate) != 5):
        print('Error: Date not valid')
        inputs()


    for element in newdate:
        if (not len(element) == 2):
            if (not(element == newdate[2] and len(element)==4)):
                print('Error: Date not valid')
                inputs()
        try:
            a = int(element)
        except Exception as e:
            print('Error: Date not valid, ' + str(e))
            inputs()


    return newdate

def check_post():
    try:
        
        print('AUTO-POST MODE ACTIVATED')
        print('I will check date and time every minute to see wheter there\'s something to post or not. Press CTRL+C to exit anytime.')
        
        while True:
            when = datetime.now()
            when = when.strftime("%d/%m/%Y %H:%M")
            now=fix_date(when)
            print('[*]\t\tCHECKING IF THERE\'S SOMETHING TO POST\t\t[*]')
            for p in posts:
                if (p.date == now):
                    print(f'It\'s time to post something...\nPOST:\nDescription: {p.description}\nPath: {p.path}\nDate: {p.date}')
                    print(p.path[len(p.path)-3:].lower())
                    if(p.path[len(p.path)-3:].lower()=='mp4'):
                        delay = os.path.getsize(p.path)*0.000001*0.6
                        upload_vid(username, password, p.path, p.description)
                    else:
                        upload(username, password, p.path, p.description)

            time.sleep(60)
    except KeyboardInterrupt as e:
        print('Going back...')
        inputs()
    except Exception as e:
        print('Error: ' + str(e))
    check_post()



def plan_post():

    global posts
    #Get new post info

    print('Post title (it will be displayed if it will be posted as an IGTV video)')
    title=input('Title: ')

    #file path
    print('Insert the image in the directory post_files, then enter the image name. If you want to go back any time in any field, write \'$\' and press enter.')
    img_path = input('File name: ')

    if(go_back(img_path)):
        inputs()

    #get the absolute path
    img_path = os.path.abspath('post_files/' + img_path)

    
    #if file not found
    if(not os.path.isfile(img_path)):
        print('Error: File not found')
        plan_post()

    #get post desciption
    print('Insert the full post description')
    desc = input('Description: ')

    if(go_back(desc)):
        inputs()

    #get post publish date and time
    print('When do you want to publish the post? (dd/mm/yyyy  hh:mm [24 hours format]) Example: \'19/09/2020 17:14\'')
    date = input('Date: ')

    if(go_back(date)):
        inputs()

    #format the date
    date = fix_date(date)

    

    #create new post by instanciating the class
    new_post = post(desc, date, img_path, title)
    posts.append(new_post)

    #save data
    save()


def edit_post():
    global posts
    #see posts already planned
    see_plan()

    #choose which post to edit
    print('Which post do you want to edit?[number]')
    try:
        edit=int(input('>>> '))
        print("What do you want to edit?\n1)Path\n2)Description\n3)Date")
        choice=int(input('>>> '))
    except Exception as e:
        print('Error: '+ str(e))
        edit_post()
    except BaseException as e:
        edit_post()
    #choice addressing, editing the chosen property
    if(choice==1):
        print('Insert the new path')
        posts[edit-1].path = input('>>> ')
    elif(choice==2):
        print('Insert the new description')
        posts[edit-1].description = input('>>> ')
    elif(choice==3):
        print('Insert the new date')
        posts[edit-1].date = fix_date(input('>>> '))

    #save data
    save()

    print('Plan successfully edited.')



def see_plan():
    #print posts plan
    count_post=1
    for _post in posts:
        print(f'\n\nPost {str(count_post)})\nTitle: {_post.title}\nDescription: {_post.description}\nPath: {_post.path}\nDate: {_post.date[0]}/{_post.date[1]}/{_post.date[2]} {_post.date[3]}:{_post.date[4]}')
        count_post+=1
    #if there are no posts planned
    if (len(posts)==0):
        print('There are no posts planned')


def delete_post():
    global posts
    #see what posts are planned
    see_plan()

    #choose the post to delete
    print('Which post do you want to delete [number]? Write $ to go back.')
    try:
        #delete the chosen post plan
        del_num=input('>>> ')
        if(go_back(del_num)):
            inputs()
        posts.pop(int(del_num)-1)
    except Exception as e:
        print('Error: ' + str(e))
        delete_post()

    save()


def inputs():
    #Get user input
    #what do you want to do?
    print('What do you want to do?\n0)Exit \n1)Plan a post \n2)See the posts plan \n3)Delete a planned post \n4)Auto-post mode\n5)Edit a post') 
    
    #error addressing
    try:
        choice = int(input('>>> '))
    except Exception as e:
        print('Error: ' + str(e))

    #choice addressing
    if(choice==0):
        exit()
    elif(choice == 1):
        plan_post()
        inputs()
    elif(choice == 2):
        see_plan()
        inputs()
    elif(choice==3):
        delete_post()
        inputs()
    elif(choice==4):
        check_post()
    elif(choice==5):
        edit_post()
        inputs()
    else:
        print('Error: Number not valid')
        inputs()


def read():
    global posts, info
    try:
        with open('posts_list.json') as f:
            data = json.load(f)

        for titles in data:
            posts.append(post(data[titles]["description"],fix_date(data[titles]["date"]), data[titles]["path"], data[titles]["title"]))
    except Exception as e:
        print('File not found, not valid or empty')

    # for p in posts:
    #     print(f'\n-{p.description}\n-{p.path}\n-{p.date}\n')

def login():
    global username,password
    #Get credentials
    print('Insert your instagram credentials') #CREDENTIALS
    username=input('username: ')
    password=getpass('password: ')
    print('\n'*10)
    read()
    inputs()




login()
from lxml import html
from getposts import getUserPosts
import requests
import pandas as pd


def getUsers(shareID):
    users = set()
    page_number = 1

    #Create a session and set the posts per page as 100
    s = requests.Session()
    s.get('https://www.lse.co.uk/ShareChat.asp?ShareTicker=' + shareID + '&page=' + str(page_number) + '&page-size=100', allow_redirects=True)

    while(True):
        print(page_number)
        page = s.get('https://www.lse.co.uk/ShareChat.asp?ShareTicker=' + shareID + '&page=' + str(page_number))
        posts = html.fromstring(page.content)

        page_users = posts.xpath('//p[@class="share-chat-message__details share-chat-message__details--username"]/a[@class="share-chat-message__link"]/text()')

        for user in page_users:
            users.add(user)
        page_number += 1

        if posts.xpath('//a[@class="pager__link pager__link--next pager__link--disabled"]'):
            break
        try:
            time.sleep(0.5)
        except:
            continue

    return users



def getPostsForAllUsers():
    users_and_posts = pd.DataFrame(columns = ['username' , 'comment'])
    shareID = ''
    users = getUsers(shareID)
    users_file_name = shareID + '_Users.txt'

    with open("users_file_name", "w") as output:
        output.write(str(users))

    for user in users:
        print("Getting posts for user: " + user)
        users_and_posts = pd.concat([users_and_posts, getUserPosts(user)], ignore_index=True)

    return users_and_posts


if __name__ == "__main__":
    df = getPostsForAllUsers()
    print(df)
    df.to_csv('all_comments.csv', index = None)

from lxml import html
import requests
import json
import pandas as pd



def getUserPosts(username):
    all_posts = []
    user_array = []
    page_number = 1
    while(True):
        page = requests.get('https://www.lse.co.uk/profiles/' + username + '/?page=' + str(page_number))
        posts = html.fromstring(page.content)
        print(page_number)

        posts_on_page = posts.xpath('//div[@class="share-chat-message__content-message"]/p')
        for post in posts_on_page:
            user_array.append(username)
            all_posts.append(post.text_content())

        page_number += 1

        if posts.xpath('//a[@class="pager__link pager__link--next pager__link--disabled"]'):
            break
        try:
            time.sleep(0.5)
        except:
            continue

    df = pd.DataFrame({"username":user_array , "comment":all_posts})

    return df


if __name__ == "__main__":
    username = input('Enter user:')
    posts_df = getUserPosts(username)

    print(posts_df)

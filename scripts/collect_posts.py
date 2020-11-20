import argparse
import json
import os
import requests

"""
Fetch hottest posts for currently for subreddit and write to a file 
"""
def write_hot_posts_to_file(file, subreddit, goal_posts = 500):
    num_posts = 100 # Fetch 100 posts 5 times using pagination
    after = ''
    num_posts = 0
    while True:
        afterText = ''
        if after:
            afterText = f'&after={after}'
        response = requests.get(
            f'http://api.reddit.com{subreddit}/hot?limit={num_posts}' + afterText,
            headers = {
                'User-Agent': 'windows: requests (by {redacted})'
            }
        ).json()
        
        after = response['data']['after']
        posts = response['data']['children']

        # Write each post to an individual file line
        isBreak = False
        for post in posts:
            file.write(json.dumps(post['data']) + '\n')
            num_posts += 1
            if num_posts >= goal_posts: # Deal with stickied posts
                isBreak = True
                break
        if isBreak:
            break

def main():
    parser = argparse.ArgumentParser()    
    
    # Specify arguments that parser takes
    parser.add_argument('-o', '--output', required=True, help='Path to output posts to')
    parser.add_argument('subreddit', help='subreddit to grab hottest posts from')

    # Parse arguments 
    args = parser.parse_args()
    
    # Open output files in write mode
    output = open(args.output, 'w')
    
    # Fetch posts
    write_hot_posts_to_file(output, args.subreddit)
       
    # Close output files
    output.close()

if __name__ == '__main__':
    main()

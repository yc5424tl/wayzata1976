import os 
from googleapiclient import discovery, errors

api_key = os.environ('YOUTUBE_API_KEY')

youtube = discovery.build('youtube', 'v3', developerKey=api_key)


def keyword_search(keyword):
    req = youtube.search().list(q=keyword, part='snippet', type='video', maxResults=1, pageToken=None)
    res = req.execute()
    video_id = res['items'][0]['id']['videoId']
    embed_url = f'https://www.youtube.com/embed/{video_id}'











# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=1,
        q=""chicago" "if you leave me now""
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()



    #### RESPONSE ######
    {
#   "kind": "youtube#searchListResponse",
#   "etag": "tY33LnM78GBJAegg-g2yI0GSlZA",
#   "nextPageToken": "CAEQAA",
#   "regionCode": "US",
#   "pageInfo": {
#     "totalResults": 366914,
#     "resultsPerPage": 1
#   },
#   "items": [
#     {
#       "kind": "youtube#searchResult",
#       "etag": "_F70vXng1NC15Qb4hYT2KKeUWWE",
#       "id": {
#         "kind": "youtube#video",
#         "videoId": "cYTmfieE8jI"
#       },
#       "snippet": {
#         "publishedAt": "2014-02-12T17:59:57Z",
#         "channelId": "UC20W_trF3L4fqmNqLoslnqw",
#         "title": "Chicago If You Leave Me Now HQ    !!!",
#         "description": "",
#         "thumbnails": {
#           "default": {
#             "url": "https://i.ytimg.com/vi/cYTmfieE8jI/default.jpg",
#             "width": 120,
#             "height": 90
#           },
#           "medium": {
#             "url": "https://i.ytimg.com/vi/cYTmfieE8jI/mqdefault.jpg",
#             "width": 320,
#             "height": 180
#           },
#           "high": {
#             "url": "https://i.ytimg.com/vi/cYTmfieE8jI/hqdefault.jpg",
#             "width": 480,
#             "height": 360
#           }
#         },
#         "channelTitle": "keyloginhot",
#         "liveBroadcastContent": "none",
#         "publishTime": "2014-02-12T17:59:57Z"
#       }
#     }
#   ]
# }



# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id="cYTmfieE8jI"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()


    ### response ####

#     {
#   "kind": "youtube#videoListResponse",
#   "etag": "MkgMt0e6ycyHG2r3iTRzmj_3BvA",
#   "items": [
#     {
#       "kind": "youtube#video",
#       "etag": "BQcqe74AAuhhLcsIq8L8s3D3l0o",
#       "id": "cYTmfieE8jI",
#       "snippet": {
#         "publishedAt": "2014-02-12T17:59:57Z",
#         "channelId": "UC20W_trF3L4fqmNqLoslnqw",
#         "title": "Chicago If You Leave Me Now HQ    !!!",
#         "description": "",
#         "thumbnails": {
#           "default": {
#             "url": "https://i.ytimg.com/vi/cYTmfieE8jI/default.jpg",
#             "width": 120,
#             "height": 90
#           },
#           "medium": {
#             "url": "https://i.ytimg.com/vi/cYTmfieE8jI/mqdefault.jpg",
#             "width": 320,
#             "height": 180
#           },
#           "high": {
#             "url": "https://i.ytimg.com/vi/cYTmfieE8jI/hqdefault.jpg",
#             "width": 480,
#             "height": 360
#           }
#         },
#         "channelTitle": "keyloginhot",
#         "tags": [
#           "antonyfoot"
#         ],
#         "categoryId": "10",
#         "liveBroadcastContent": "none",
#         "localized": {
#           "title": "Chicago If You Leave Me Now HQ    !!!",
#           "description": ""
#         }
#       },
#       "contentDetails": {
#         "duration": "PT4M",
#         "dimension": "2d",
#         "definition": "sd",
#         "caption": "false",
#         "licensedContent": false,
#         "contentRating": {},
#         "projection": "rectangular"
#       },
#       "statistics": {
#         "viewCount": "19612567",
#         "likeCount": "114417",
#         "dislikeCount": "3117",
#         "favoriteCount": "0",
#         "commentCount": "5466"
#       }
#     }
#   ],
#   "pageInfo": {
#     "totalResults": 1,
#     "resultsPerPage": 1
#   }
# }

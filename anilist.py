import requests
from io import StringIO
import json
from bs4 import BeautifulSoup
def search_anilist(search, type, max_results=10):
  query = """
  query ($id: Int, $page: Int, $search: String, $type: MediaType) {
      Page (page: $page, perPage: 10) {
          media (id: $id, search: $search, type: $type) {
              id
              idMal
              description(asHtml: false)
              title {
                  english
                  romaji
              }
              coverImage {
                  extraLarge
              }
              bannerImage
              averageScore
              status
              episodes
              chapters
              externalLinks {
                  url
                  site
              }
          }
      }
  }
  """
  variables = {
      'search': search,
      'page': 1,
      'perPage': max_results,
      'type': type
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  io = StringIO(response.text)
  results = json.load(io)
  try:
    result_list = results['data']['Page']['media']
    final_result = []
    for anime in result_list:
      title = anime['title']['romaji']
      ani_id = anime['id']
      status = anime['status']
      thumbnail = anime['coverImage']['extraLarge']
      episodes = anime['episodes']
      description = anime['description'].replace('<br>', '').replace('\\', '').replace('/', '').replace('"', '').replace('<i>', '').replace('\n', '')
      if type == 'ANIME':
        link = f'https://anilist.co/anime/{ani_id}'
      if type == 'MANGA':
        link = f'https://anilist.co/manga/{ani_id}'
      entry = {"title": title, "id": ani_id, "link": link, "episodes": episodes, "status":status, "description": description, "picture": thumbnail}
      final_result.append(entry)
  except:
    final_result = results['errors'][0]['message']
    raise Exception(final_result)
  return final_result

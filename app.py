from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def modify_str(orignal):
    name = orignal.split(" ")
    # print(name)
    # print("+".join(name))
    return "+".join(name)

@app.route("/")
def start():
    return jsonify({'status':200, 'messgae': 'Server is running!'}), 200


@app.route("/test", methods=['POST'])
def test():
    if request.method == "POST":
        try:
            modify_str(request.get_json()['query'])
            response = requests.get(f"https://myneta.info/search_myneta.php?q={modify_str(request.get_json()['query'])}")
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_="w3-table w3-striped w3-bordered")
            
            if table is None:
                return jsonify({'status':404, 'error': 'Table not found!!'}), 404
            # print(rows)
            rows = table.find_all('tr')[1:]

            candidates = []


            try:
                for row in rows:
                    cols = row.find_all('td')


                    # Skip if there are not enough columns
                    if len(cols) < 5:
                        continue

                    img_tag = cols[0].find('img')
                    img_url = img_tag['src'] if img_tag else None

                    candidate_link_tag = cols[0].find('a')
                    candidate_name = candidate_link_tag.text.strip() if candidate_link_tag else None
                    candidate_profile_url = candidate_link_tag['href'] if candidate_link_tag else None

                    party = cols[-4].text.strip()
                    constituency = cols[-3].text.strip()
                    election = cols[-2].text.strip()
                    criminal_case = cols[-1].text.strip()

                    candidate_info = {
                        'image_url': img_url,
                        'candidate_name': candidate_name,
                        'candidate_profile_url': f"https://myneta.info{candidate_profile_url}",
                        'party': party,
                        'constituency': constituency,
                        'election': election,
                        'criminal_case': criminal_case
                    }

                    candidates.append(candidate_info)

                # data = response.text
                # data = request.get_json()
                return jsonify({'status':200, 'data': candidates}), 200
            except AttributeError as e:
                return jsonify({'status':500, 'error': str(e)}), 500
            
        except requests.RequestException as e:
            # print(e)
            return jsonify({'status':500, 'error': str(e)}), 500

        






import requests, csv
from bs4 import BeautifulSoup

date = input("Please enter the date in the format of (MM/DD/YYYY):\n")
filename = input("Please enter the name of the file you want to save the data in ['filename.csv']:\n")
page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

src = page.content
soup = BeautifulSoup(src, 'lxml')
matchesList = []

def writeCSV(matchesList):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['البطوله', 'الفريق الاول', 'النتيجه', 'الفريق الثانى', 'الحاله', 'الوقت', 'التاريخ'])
        writer.writeheader()
        writer.writerows(matchesList)
        
def fetchMatches():
    championships = soup.find_all('div', {'class': 'matchCard'})
    for championship in championships:
        championshipTitle = championship.find('div', {'class': 'title'}).find('h2').text.strip().replace('..', '')
        matches = championship.find('div', {'class': 'ul'}).find_all('div', {'class': 'item'})
        for match in matches:
            matchStatus = match.find('a').find('div', {'class': 'matchStatus'}).find('span').text.strip()
            teamA = match.find('a').find('div', {'class': 'teamA'}).find('p').text.strip()
            teamB = match.find('a').find('div', {'class': 'teamB'}).find('p').text.strip()
            teamAScore = match.find('a').find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})[0].text.strip()
            teamBScore = match.find('a').find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})[1].text.strip()
            time = match.find('a').find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()
            matchesList.append({
                'البطوله': championshipTitle, 
                'الفريق الاول': teamA, 
                'النتيجه': f"{teamAScore}-{teamBScore}", 
                'الفريق الثانى': teamB, 
                'الحاله': matchStatus,
                'الوقت': f'{date} - {time}', 
                'التاريخ' : date
                })


fetchMatches()
writeCSV(matchesList)
    
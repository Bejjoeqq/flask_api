import requests
import json
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/87.0.4280.141",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive"
}
def cari_nama(nama,dosen=False):
    url = "https://dinus.ac.id//search/"
    with requests.session() as session:
        asw = ("nama=" + nama + "&kategori=People&search=")

        r_post = session.post(url, data=asw, headers=headers)

    src = r_post.content
    soup = BeautifulSoup(src, "html.parser")

    namamhs = []
    nimmhs = []
    for nama in soup.find_all("a", style="font-size: 1.1em;"):
        if dosen:
            if "detailstaf" in nama["href"]:
                namamhs.append(nama.text)
                nimmhs.append(nama["href"].replace("https://dinus.ac.id/detailstaf/",""))
        else:
            if "mahasiswa" in nama["href"]:
                namamhs.append(nama.text)
                nimmhs.append(nama["href"].replace("https://dinus.ac.id/mahasiswa/",""))
    return nimmhs,namamhs

def dosen(npp,nimmhs):
    url = f"https://dinus.ac.id/detailstaf/{npp}"
    response = requests.get(url,headers=headers).content
    soup = BeautifulSoup(response,"html.parser")

    table = soup.find("table", "table")
    nama = table.find_all("tr")[0].find_all("td")[-1].text
    nidn = table.find_all("tr")[2].find_all("td")[-1].text
    jabatan = table.find_all("tr")[4].find_all("td")[-1].text
    statustaf = table.find_all("tr")[5].find_all("td")[-1].text
    golongan = table.find_all("tr")[6].find_all("td")[-1].text
    emaildos = table.find_all("tr")[7].find_all("td")[-1].text
    ipk = soup.body.find(text=nimmhs).parent.parent.find_all("td")[-1].text
    return nama,ipk,nidn,jabatan,statustaf,golongan,emaildos.replace("\n","").split()

def detail_academic(nimmhs):
    url = f"http://academic.dinus.ac.id/home/data_mahasiswa/{nimmhs}"
    response = requests.get(url,headers=headers).content
    soup = BeautifulSoup(response,"html.parser")

    table = soup.find("table", "table table-striped table-hover")
    rows = table.find_all("tr")
    jk = rows[2].find_all("td")[-1].text.strip()
    ttl = rows[3].find_all("td")[-1].text.strip()
    tempat = ttl.split(",")[-2]
    tanggal = ttl.split(",")[-1].strip().split()
    return jk,tempat,tanggal

def manipulasinim(nimmhs):
    data = {
        "A": {
            "fakultas" : "Fakultas Ilmu Komputer",
            "11" : "Teknik Informatika - S1",
            "12" : "Sistem Informasi - S1",
            "22" : "Teknik Informatika - D3",
            "15" : "Ilmu Komunikasi - S1",
            "14" : "Desain Komunikasi Visual - S1",
            "16" : "Film dan Televisi - SST",
            "17" : "Animasi - SST",
            "24" : "Broadcasting - D3"
        },
        "B" : {
            "fakultas" : "Fakultas Ekonomi dan Bisnis",
            "12" : "Akuntansi - S1",
            "11" : "Manajemen - S1"
        },
        "C" : {
            "fakultas" : "Fakultas Ilmu Budaya",
            "11" : "Sastra Inggris - S1",
            "13" : "Manajemen Perhotelan - SST",
            "12" : "Sastra Jepang - S1"
        },
        "D" : {
            "fakultas" : "Fakultas Kesehatan",
            "11" : "Kesehatan Masyarakat - S1",
            "22" : "Rekam Medik & Informasi Kesehatan - D3",
            "12" : "Kesehatan Lingkungan - S1"
        },
        "E" : {
            "fakultas" : "Fakultas Teknik",
            "11" : "Teknik Elektro - S1",
            "12" : "Teknik Industri - S1",
            "13" : "Teknik Biomedis - S1"
        }
    }
    return data[nimmhs[:1]]["fakultas"],data[nimmhs[:1]][nimmhs[1:]]

def detail(nimmhs,full=True):
    resultdata = {
        "status" : 200,
        "message" : "",
        "result" : {
            "nim" : "",
            "nama" : "",
            "photo" : "",
            "status_mahasiswa" : "",
            "dosen_pembimbing" : {
                "npp" : "",
                "nidn" : "",
                "nama_asli" : "",
                "nama_gelar" : "",
                "jabatan":"",
                "status_staff" : "",
                "golongan" : "",
                "email_staff" : []
                },
            "email" : [],
            "agama" : "",
            "jenis_kelamin" : "",
            "lahir" : {
                "tempat" : "",
                "tanggal" : "",
                "bulan" : "",
                "tahun" : ""
                },
            "ipk" : "",
            "angkatan" : "",
            "program_studi" : "",
            "fakultas" : "",
            "total_sks" : "",
            "krs" : [],
            "organisasi" : [],
            "beasiswa" : []
            }
    }

    url = f"https://dinus.ac.id/mahasiswa/{nimmhs}"
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response,"html.parser")

    table = soup.find("table", "table")
    rows = table.find_all("tr")
    agm = soup.find(text="E-mail").parent.parent.find_all("td")[-1].text.strip()
    print(agm)

    resultdata["status"] = 200
    resultdata["message"] = "success"

    resultdata["result"]["nim"] = rows[1].find_all("td")[-1].text.strip()
    resultdata["result"]["nama"] = rows[0].find_all("td")[-1].text.strip()
    resultdata["result"]["photo"] = soup.find("a","fotonews").img["src"]
    resultdata["result"]["status_mahasiswa"] = rows[3].find_all("td")[-1].text.strip()
    resultdata["result"]["dosen_pembimbing"]["nama_asli"] = rows[2].find_all("td")[-1].text.strip()

    npp = cari_nama(resultdata["result"]["dosen_pembimbing"]["nama_asli"],dosen=True)[0][0]
    resultdata["result"]["dosen_pembimbing"]["npp"] = npp.strip()

    namatitle,ipk,nidn,jabatan,statustaf,golongan,emaildos = dosen(npp,resultdata["result"]["nim"])
    resultdata["result"]["dosen_pembimbing"]["nama_gelar"] = namatitle.strip()
    resultdata["result"]["dosen_pembimbing"]["nidn"] = nidn.strip()
    resultdata["result"]["dosen_pembimbing"]["jabatan"] = jabatan.strip()
    resultdata["result"]["dosen_pembimbing"]["status_staff"] = statustaf.strip()
    resultdata["result"]["dosen_pembimbing"]["golongan"] = golongan.strip()
    resultdata["result"]["dosen_pembimbing"]["email_staff"] = list(set([x.strip().replace("[a]","@") for x in emaildos]))

    email = soup.find(text="E-mail").parent.parent.find_all("td")[-1].text.replace("\n","").split()
    resultdata["result"]["email"] = list(set([x.strip().replace("[a]","@") for x in email]))
    resultdata["result"]["agama"] = rows[6].find_all("td")[-1].text.strip()

    if full:
        jk,tempat,tanggal = detail_academic(resultdata["result"]["nim"])
        resultdata["result"]["jenis_kelamin"] = jk.strip()
    else:
        jk,tempat,tanggal ="","",["","",""]

    resultdata["result"]["lahir"]["tempat"] = tempat
    resultdata["result"]["lahir"]["tanggal"] = tanggal[0]
    resultdata["result"]["lahir"]["bulan"] = tanggal[1]
    resultdata["result"]["lahir"]["tahun"] = tanggal[2]

    resultdata["result"]["ipk"] = ipk.strip()
    resultdata["result"]["angkatan"] = resultdata["result"]["nim"].split(".")[1]

    fakultass,prodi = manipulasinim(resultdata["result"]["nim"].split(".")[0])
    resultdata["result"]["program_studi"] = prodi
    resultdata["result"]["fakultas"] = fakultass

    tabledata = soup.find_all("table","table table-bordered table-striped")

    krs = tabledata[0].find_all("tr")[1:]
    total_sks = 0
    for tr in krs:
        td = tr.find_all("td")[1:]
        resultdata["result"]["krs"].append({
            "kode" : td[0].text.strip(),
            "grup_kelas" : td[1].text.strip(),
            "mata_kuliah" : td[2].text.strip(),
            "sks" : td[3].text.strip(),
            "status_kelas" : td[4].text.strip()
        })
        total_sks+=int(td[3].text.strip())

    resultdata["result"]["total_sks"] = str(total_sks)

    org = tabledata[1].find_all("tr")[1:]
    for tr in org:
        td = tr.find_all("td")[1:]
        resultdata["result"]["organisasi"].append({
            "nama_organisasi" : td[0].text.strip(),
            "status_organisasi" : td[1].text.strip(),
            "periode" : td[2].text.strip()
        })

    bswn = tabledata[-2].find_all("tr")[1:]
    for tr in bswn:
        td = tr.find_all("td")[-1]
        resultdata["result"]["beasiswa"].append(td.text.strip())

    return resultdata

if __name__ == '__main__':
    result = detail("A11.2019.12167",False)
    print(result)

    
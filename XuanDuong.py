from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException
import pandas as pd


edge_path='C:\\Users\\Admin\\OneDrive - VNU-HCMUS\\2022-2026\\Nam 2\\NMKHDL\\doan\\edgedriver_win64\\msedgedriver.exe'
driver = webdriver.Edge(edge_path)

link = "https://batdongsan.vn/ban-nha/"
driver.get(link)

data_link=[]# Data chứa các link của mỗi bài đăng
data = pd.DataFrame(columns=['Tiêu đề', 'Diện tích(m2)', 'Số phòng ngủ', 'Số phòng WC', 'Thời gian đăng', 'Tỉnh/Thành', 'Quận/Huyện', 'Hướng nhà', 'Hướng ban công','Loại nhà' ,'Giá','Link'])

def Geturl(data):  # Hàm lấy link
    elements = driver.find_elements(By.XPATH, "//*[@class='name']")
    titles = driver.find_elements(By.XPATH, "//*[@class='meta']")
    motas = driver.find_elements(By.XPATH, "//*[@class='sapo uk-hidden-small uk-hidden-medium']" )
    link_elements = driver.find_elements(By.XPATH, "//*[@class='name']/a")
    for element, title, link, mota in zip(elements, titles, link_elements, motas ):
        href = link.get_attribute('href')
        data = pd.concat([data, pd.DataFrame({
            'Tieu de': [element.text],
            'Gia': [title.text],
            'link' :[href]
        })], ignore_index=True)
        mota=mota
        data_link.append(href)
    return data

input_page = int(input('Số trang muốn lấy dữ liệu:')) # Hàm lấy link của n trang
for i in range(input_page):
  data = Geturl(data.copy()) 
  next = driver.find_element(By.XPATH, "//*[@class='uk-icon-angle-right']")
  next.click()

extracted_data = pd.DataFrame(columns=['Tiêu đề', 'Diện tích(m2)', 'Số phòng ngủ', 'Số phòng WC', 'Thời gian đăng', 'Tỉnh/Thành', 'Quận/Huyện', 'Hướng nhà', 'Hướng ban công','Loại nhà' ,'Giá','Link'])
def get_square(): # Lấy diện tích
    try: # Diện tích
        square = driver.find_element(By.XPATH, '*//*[*[text()="Diện tích:"]]').text.split() # Tách lkí tự
        if square[3] == "m2": # chỉ lấy diện tích là m^2
            square=square[2]
        else:
            square= "" 
    except: 
        square ="" 
    return square
    

def get_PN(): #Lấy số phòng ngủ
    try: #phòng ngủ
        bed =driver.find_element(By.XPATH, '*//*[*[text()="phòng ngủ:"]]').text.split()
        bed= bed[2] # lấy số  số phòng ngủ
    except:
        bed=""
    return bed

def get_WC():#Lấy số phòng WC
    try:  #phòng WC
        WC= driver.find_element(By.XPATH, '*//*[*[text()="phòng WC:"]]').text.split()
        WC= WC[2]# lấy ra số lượng WC
    except:
        WC=""
    return WC

def get_time(): # Lấy Thời gian đăng 
    try:
        time = driver.find_element(By.XPATH, '//*[@class="timeago"]')
        time = time.get_attribute("title").split()[1]
    except :
        time=""
    return time

def get_address_tinh(): # Lấy tên tỉnh
    a=driver.find_element(By.XPATH, '//*[@id="post-detail"]/body/div[4]/div/div/ul/li[3]/a').text
    return a

def get_address_huyen(): # Lấy tên huyện
    b= driver.find_element(By.XPATH, '//*[@id="post-detail"]/body/div[4]/div/div/ul/li[4]/a').text
    return b

def get_price(): # Lấy giá ( quy đổi về tỷ)
    price = driver.find_element(By.XPATH, '//*[@id="post-detail"]/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/strong').text
    a = price.split()
    if a[1] == "triệu": 
        price = float(a[0]) / 1000
    elif a[1] == "tỷ":
        price = float(a[0])
    else:
        price=""
    return price

def get_loainha(): #Lấy loại nhà
    b=driver.find_element(By.XPATH, '//*[@id="post-detail"]/body/div[4]/div/div/ul/li[2]/a').text
    return b

def get_huongnha(): #Lấy hướng nhá
    try:
        huong= driver.find_element(By.XPATH, '*//*[*[text()="Hướng nhà:"]]').text.split()
        huong=huong[2]
    except:
        huong=""
    return huong
        
def get_huongbancong(): # Lấy hướng ban công
    try:
        huong= driver.find_element(By.XPATH, '*//*[*[text()="Hướng ban công:"]]').text.split()
        huong=huong[3]
    except:
        huong=""
    return huong

def crawl_website(url): # hàm lấy thông tin từng cái
    title = driver.find_element(By.XPATH, "//*[@id='post-detail']/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/h1").text
    square = get_square()  # Hàm lấy diện tích
    bed = get_PN()  # Hàm lấy số phòng ngủ
    WC = get_WC()  # Hàm lấy số phòng WC
    time = get_time()  # Hàm lấy thời gian đăng
    dn = get_address_tinh()  # Hàm lấy tỉnh/thành
    tp = get_address_huyen()  # Hàm lấy quận/huyện
    price = get_price()  # Hàm lấy giá
    huong_nha=get_huongnha()
    huong_ban_cong=get_huongbancong()
    loainha=get_loainha()
    #Tạo DataFrame
    extracted_data = pd.DataFrame({
        'Tiêu đề': [title],
        'Diện tích(m2)': [square],
        'Số phòng ngủ': [bed],
        'Số phòng WC': [WC],
        'Thời gian đăng': [time],
        'Tỉnh/Thành': [dn],
        'Quận/Huyện': [tp],
        'Hướng nhà': [huong_nha], 
        'Hướng ban công': [huong_ban_cong],
        'Loại nhà':[loainha] ,
        'Giá': [price],
        'Link': [url],
    })
    
    return extracted_data


# Khởi tạo danh sách để chứa các DataFrame con
all_extracted_data = []

# Lặp qua danh sách data_link và trích xuất dữ liệu từ mỗi link
for link in data_link:
    driver.get(link)
    extracted_data = crawl_website(link)
    all_extracted_data.append(extracted_data)  # Thêm DataFrame con vào danh sách

# Kết hợp tất cả các DataFrame con thành một DataFrame lớn
final_extracted_data = pd.concat(all_extracted_data, ignore_index=True)

#Chuyển vào file csv
final_extracted_data.to_csv("data1.csv", encoding='utf-8-sig', index=False)


SRC_PATH = "https://www.thegioididong.com/laptop#c=44&o=13&pi="

#Số lượng sản phẩm cần lấy thông tin thì chỉnh ở đây
PRODUCT_INFO_NEED = 300


PRODUCTS_IN_ONE_PAGE = 20

def compute_page_need() -> int:
    return PRODUCT_INFO_NEED // PRODUCTS_IN_ONE_PAGE  if PRODUCT_INFO_NEED % PRODUCTS_IN_ONE_PAGE == 0 else PRODUCT_INFO_NEED // PRODUCTS_IN_ONE_PAGE + 1


REAL_PATH = SRC_PATH + str(compute_page_need())

PREFIX_PRODUCT_URL = "https://www.thegioididong.com"


SLEEP_TIME = 0.01

SAVE_DIR = 'data'


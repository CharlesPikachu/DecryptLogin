'''
Function:
	QQ个人专属报告生成
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import warnings
from modules.utils import *
from modules.QQReports import QQReports
warnings.filterwarnings('ignore')


'''一些常量'''
FONT_PATH = 'material/font.TTF'
DATA_SAVE_DIR = 'qqdata'
RESULTS_SAVE_DIR = 'results'
PERSONAL_INFO_FILENAME = 'personal_info'
PERSONAL_INFO_BG_PATH = 'material/personalcard.jpg'
FRIENDS_INFO_FILENAME = 'friends_info'
RECENT_OPERATIONS_INFO_FILENAME = 'recent_operation_info'
RECENT_OPERATIONS_INFO_BG_PATH = 'material/recentcard.jpg'
checkDir(DATA_SAVE_DIR)
checkDir(RESULTS_SAVE_DIR)


'''下载所有需要的数据'''
def getReportsData():
	qq_reports = QQReports(DATA_SAVE_DIR)
	# 个人基本信息
	personal_info = qq_reports.getPersonalInfo(PERSONAL_INFO_FILENAME+'.pkl')
	makePersonalCard(personal_info, PERSONAL_INFO_BG_PATH, savepath=os.path.join(RESULTS_SAVE_DIR, PERSONAL_INFO_FILENAME+'.jpg'), fontpath=FONT_PATH)
	# 好友信息
	friends_info = qq_reports.getQQFriendsInfo(FRIENDS_INFO_FILENAME+'.pkl')
	nicknames = [value[0] for value in friends_info.values()]
	nicknames = dict(zip(nicknames, [1]*len(nicknames)))
	drawWordCloud(nicknames, savepath=os.path.join(RESULTS_SAVE_DIR, FRIENDS_INFO_FILENAME+'.jpg'), font_path=FONT_PATH)
	# 最近操作信息
	recent_operation_info = qq_reports.getRecentOperationsInfo(RECENT_OPERATIONS_INFO_FILENAME+'.pkl')
	makeRecentCard(friends_info, recent_operation_info, RECENT_OPERATIONS_INFO_BG_PATH, savepath=os.path.join(RESULTS_SAVE_DIR, RECENT_OPERATIONS_INFO_FILENAME+'.jpg'), fontpath=FONT_PATH)


'''run'''
if __name__ == '__main__':
	getReportsData()
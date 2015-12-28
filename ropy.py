import json, pycurl, io, os, hashlib, re, urllib

from StringIO import StringIO
from bs4 import BeautifulSoup
from datetime import date

class RoPy:
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	strCookieJar = 'cookies'
	currentUser = ''
	boolDebug = False

	def Debug(self, d1, d2):
		if d1 is not 3:
			print '[{0}]: {1}'.format(d1, d2)

	def GetCountry(self, strCountry):
		try:
			arrList = json.loads(open(os.path.join(__location__, 'countries.json'), 'r').readline())

			return arrList[strCountry]
		except:
			return 1

	def GetPrivacySetting(self, strType, intID):
		try:
			arrList = json.loads(open(os.path.join(__location__, 'privacy.json'), 'r').readline())

			return arrList[strType][intID]
		except:
			return False

	def GetGenreSetting(self, strType):
		try:
			arrList = json.loads(open(os.path.join(__location__, 'genre.json'), 'r').readline())

			return arrList[strType]
		except:
			return 1

	def GetGender(self, strGender):
		if strGender.upper() == "FEMALE":
			return 3

		return 2

	def GetLanguage(self, strLanguage):
		if strLanguage.upper() == 'GERMAN':
			return 3

		return 1

	def RemoveCookie(self, strUser):
		try:
			os.remove(os.path.join(self.__location__, self.strCookieJar, hashlib.md5(strUser).hexdigest()))
		except:
			return False

	def GetCookie(self, strUser):
		try:
			return os.path.join(self.__location__, self.strCookieJar, hashlib.md5(strUser).hexdigest())
		except:
			return False

	def GetToken(self, strToken):	
		if strToken == 'VERIFICATION':
			m = re.search('\<input name="__RequestVerificationToken" type="hidden" value="(.*?)"', self.NetworkRequest('https://m.roblox.com/home', None, True))
		elif strToken == 'CSRF':
			m = re.search("Roblox\.XsrfToken\.setToken\('(.*?)'\)", self.NetworkRequest('http://www.roblox.com/home', None, True))
		else:
			m = re.search('\<input type="hidden" name="'+strToken+'" id="'+strToken+'" value="(.*?)"' , cachedPage)

		try:
			return m.group(1)
		except:
			return False

	def NetworkRequest(self, strURL, arrData = None, boolCookie = False, strToken = None):
		buffer = StringIO()
		c = pycurl.Curl()

		c.setopt(c.URL, strURL)
		c.setopt(c.REFERER, strURL)
		c.setopt(c.USERAGENT, 'Googlebot/2.1')
		c.setopt(c.SSL_VERIFYPEER, False)
		c.setopt(c.FOLLOWLOCATION, True)

		if self.boolDebug is True:
			c.setopt(c.DEBUGFUNCTION, self.Debug)
			c.setopt(c.VERBOSE, 1)

		if arrData is not None:
			c.setopt(c.POSTFIELDS, urllib.urlencode(arrData))

		if boolCookie is True:
			c.setopt(c.COOKIEFILE, self.GetCookie(self.currentUser))
			c.setopt(c.COOKIEJAR, self.GetCookie(self.currentUser))

		if strToken is not None:
			c.setopt(c.HTTPHEADER, ['Connection: keep-alive', 'X-CSRF-TOKEN: ' + strToken, 'X-Requested-With: XMLHttpRequest',])

		c.setopt(c.WRITEDATA, buffer)
		c.perform()
		c.close()

		return buffer.getvalue()

	#
	#	User API
	#

	def GetUserID(self, strName):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/users/get-by-username?username=' + strName))['Id']
		except:
			return False

	def GetUsername(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/users/' + `intID`))['Username']
		except:
			return False

	def GetUsernames(self, intID):
		try:
			soup = BeautifulSoup(self.NetworkRequest('http://www.roblox.com/users/' + `intID` + '/profile'), 'html.parser')

			return [element['data-original-title'].split(',') for element in soup.find_all('span', {'data-toggle' : 'tooltip'})]
		except:
			return False

	def GetUserAbout(self, intID):
		try:
			soup = BeautifulSoup(self.NetworkRequest('http://www.roblox.com/users/' + `intID` + '/profile'), 'html.parser')

			return soup.find_all('span', {'class' : 'profile-about-content-text'})[0].text
		except:
			return False

	def GetUserAge(self, intID):
		try:
			soup = BeautifulSoup(self.NetworkRequest('http://www.roblox.com/users/' + `intID` + '/profile'), 'html.parser')

			return soup.find_all('p', {'class' : 'rbx-lead'})[0].text
		except:
			return False

	def IsFollower(self, intID, intTarget):
		try:
			return True if 'true' in json.loads(self.NetworkRequest('http://api.roblox.com/user/following-exists?userId=' + `intID` + '&followerUserId=' + `intTarget`, None, True))['isFollowing'] else False
		except:
			return False

	def IsFriend(self, intID, intTarget):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsFriendsWith&playerId=' + `intID` + '&userId=' + `intTarget`) else False
		except:
			return False

	def GetUserPlaces(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/Contests/Handlers/Showcases.ashx?userId=' + `intID`))['Showcase']
		except:
			return False

	#
	#	Group API
	#

	def GetGroupInfo(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID`))
		except:
			return False

	def GetGroupOwner(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID`))['Owner']['Id']
		except:
			return False

	def GetGroupName(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID`))['Name']
		except:
			return False

	def GetGroupMemberCount(self, intID):
		try:
			soup = BeautifulSoup(self.NetworkRequest('http://www.roblox.com/Groups/group.aspx?gid=' + `intID`), 'html.parser')

			return [element.text.replace('Members: ', '') for element in soup.find_all('div', {'id' : 'MemberCount'})]
		except:
			return False

	def GetGroupDescription(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID`))['Description']
		except:
			return False

	def GetGroupImg(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID`))['EmblemUrl']
		except:
			return False

	def GetGroupEnemies(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID` + '/enemies'))['Groups']
		except:
			return False

	def GetGroupAllies(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/groups/' + `intID` + '/allies'))['Groups']
		except:
			return False

	def GetGroupRoles(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/api/groups/' + `intID` + '/RoleSets'))
		except:
			return False

	def IsInGroup(self, intID, intTarget):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsInGroup&playerid=' + `intTarget` + '&groupid=' + `intID`))
		except:
			return False	

	def GetUserRank(self, intID, intTarget):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=' + `intTarget` + '&groupid=' + `intID`))
		except:
			return False	

	def GetUserRankID(self, intID, intTarget):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid=' + `intTarget` + '&groupid=' + `intID`))
		except:
			return False	

	def GetPrimaryGroup(self, strUser):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx?users=' + strUser))
		except:
			return False	

	#
	#	Auth API [User]
	#

	def DoLogin(self, strPassword):
		try:
			return True if '<head><title>Object moved</title></head>' in self.NetworkRequest('https://m.roblox.com/login', {'UserName' : self.currentUser ,'Password' : strPassword, 'IdentificationCode': ''}, True) else False
		except:
			return False

	# DOES NOT REMOVE & INVALIDATE COOKIE!
	def Logout(self):
		try:
			self.NetworkRequest('https://www.roblox.com/MobileAPI/Logout', {}, True)
		except:
			return False

	def IsLoggedIn(self):
		try:
			if not 'null' in self.NetworkRequest('http://www.roblox.com/Game/GetCurrentUser.ashx', None, True):
				return True

			self.RemoveCookie(self.currentUser)
			return False
		except:
			return False

	def ModifyAccount(self, strPersonalBlurb, boolNewsletter, intBirthDay, intBirthMonth, intBirthYear, strGender, strCountry, strLanguage, strYouTube, strTwitch, intSocialNetworksVisibilityPrivacy, intPrivateMessagePrivacy, intPrivateServerInvitePrivacy, intFollowMePrivacy):
		try:
			return True if 'succ=true' in self.NetworkRequest('https://www.roblox.com/my/account/update', {'__RequestVerificationToken': self.GetToken('VERIFICATION'), 'ReceiveNewsletter': boolNewsletter, 'BirthDay': intBirthDay, 'BirthMonth': intBirthMonth, 'BirthYear': intBirthYear, 'Gender': GetGender(strGender), 'CountryId': GetCountry(strCountry), 'strLanguage': GetLanguage(strLanguage), 'YouTube': strYouTube, 'Twitch': strTwitch, 'SocialNetworksVisibilityPrivacy': GetPrivacySetting(intSocialNetworksVisibilityPrivacy), 'PrivateMessagePrivacy': GetPrivacySetting(intPrivateMessagePrivacy), 'PrivateServerInvitePrivacy': GetPrivacySetting(intPrivateServerInvitePrivacy), 'FollowMePrivacy': GetPrivacySetting(intFollowMePrivacy)},True) else False
		except:
			return False

	def ChangePassword(self, strOldPassword, strNewPassword):
		try:
			return True if 'true' in self.NetworkRequest('https://www.roblox.com/account/changepassword', {'oldPassword': strOldPassword, 'newPassword': strNewPassword, 'confirmNewPassword': strNewPassword}, True, self.GetToken('CSRF')) else False
		except:
			return False

	def GetUserFunds(self):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/my/balance', None, True))
		except:
			return False

	def SetFeeling(self, strFeeling):
		try:
			return True if self.NetworkRequest('http://m.roblox.com/Account/SetStatus', {'__RequestVerificationToken': self.GetToken('VERIFICATION'), 'Status': strFeeling}, True) == 'true' else False
		except:
			return False

	def SetPlaceState(self, intID, boolState):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/build/set-place-state?placeId=' + `intID` + '&active=' + `boolState`, None, True, self.GetToken('CSRF')) else False
		except:
			return False

	def SendMessage(self, intID, strSubject, strContent):
		try:
			return True if 'Your message has been sent to' in self.NetworkRequest('http://m.roblox.com/messages/sendmessagework', {'__RequestVerificationToken': self.GetToken('VERIFICATION'), 'RecipientId': `intID`, 'Subject': strSubject, 'Body': strContent}, True) else False
		except:
			return False

	def GetMessages(self, intPage, intPageSize):
		try:
			return json.loads(self.NetworkRequest('http://www.roblox.com/messages/api/get-messages?messageTab=0&pageNumber=' + `intPage` + '&pageSize=' + `intPageSize`, None, True))
		except:
			return False

	def GetUnreadMessages(self):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/incoming-items/counts', None, True))['unreadMessageCount']
		except:
			return False

	def SendFriendRequest(self, intID):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/friends/sendfriendrequest', {'targetUserId': `intID`}, True, self.GetToken('CSRF')) else False
		except:
			return False

	def FollowUser(self, intID):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/user/follow', {'targetUserId': `intID`}, True, self.GetToken('CSRF')) else False
		except:
			return False

	def UnfollowUser(self, intID):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/user/unfollow', {'targetUserId': `intID`}, True, self.GetToken('CSRF')) else False
		except:
			return False

	def BlockUser(self, intID):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/userblock/blockuser', {'blockeeId': `intID`}, True, self.GetToken('CSRF')) else False
		except:
			return False

	def UnblockUser(self, intID):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/userblock/unblockuser', {'blockeeId': `intID`}, True, self.GetToken('CSRF')) else False
		except:
			return False

	#
	#	Auth API [Group]
	#

	def SetGroupShout(self, intID, strMessage):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, {'__RequestVerificationToken': self.GetToken('VERIFICATION', cache), '__VIEWSTATE': self.GetToken('__VIEWSTATE', cache), '__EVENTARGUMENT': self.GetToken('__EVENTARGUMENT', cache), '__EVENTVALIDATION': self.GetToken('__EVENTVALIDATION', cache), 'ctl00$cphRoblox$GroupStatusPane$StatusTextBox': strMessage, 'ctl00$cphRoblox$GroupStatusPane$StatusSubmitButton': 'Group Shout'}, True)
		except:
			return False

	def SetGroupRole(self, intID, intTarget, strRole):
		try:
			if isinstance( strRole, (int, long) ):
				self.NetworkRequest('http://www.roblox.com/groups/api/change-member-rank?groupId=' + `group` + '&newRoleSetId=' + `strRole` + '&targetUserId=' + `intTarget`, None, True, self.GetToken('CSRF'))
			else:
				for arrRole in GetGroupRoles(intID):
					if arrRole['Name'] == strRole:
						self.NetworkRequest('http://www.roblox.com/groups/api/change-member-rank?groupId=' + `group` + '&newRoleSetId=' + `arrRole['ID']` + '&targetUserId=' + `intTarget`, None, True, self.GetToken('CSRF'))
		except:
			return False

	def KickFromGroup(self, intID, intTarget):
		try:
			self.NetworkRequest('http://www.roblox.com/group/kick-from-clan', {'userIdToKick': `intTarget`,'groupId': `intID`, '__RequestVerificationToken': self.GetToken('VERIFICATION')}, True)
		except:
			return False

	def LeaveGroup(self, intID):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, {'__RequestVerificationToken': self.GetToken('VERIFICATION', cache), '__VIEWSTATE': self.GetToken('__VIEWSTATE', cache), '__EVENTARGUMENT': self.GetToken('__EVENTARGUMENT', cache), '__EVENTVALIDATION': self.GetToken('__EVENTVALIDATION', cache), 'ctl00$cphRoblox$GroupStatusPane$LeaveButton': 'Leave Group'}, True)
		except:
			return False

	def JoinGroup(self, intID):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/Groups/Group.aspx?gid=' + `intID`, None, True)

			self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, {'__RequestVerificationToken': self.GetToken('VERIFICATION', cache), '__VIEWSTATE': self.GetToken('__VIEWSTATE', cache), '__EVENTARGUMENT': 'Click', '__EVENTTARGET': 'JoinGroupDiv', '__EVENTVALIDATION': self.GetToken('__EVENTVALIDATION', cache)}, True)
		except:
			return False

	def MakePrimary(self, intID):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Group.aspx?gid=' + `intID`, None, True)

			self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, {'__RequestVerificationToken': self.GetToken('VERIFICATION', cache), '__VIEWSTATE': self.GetToken('__VIEWSTATE', cache), '__EVENTARGUMENT': self.GetToken('__EVENTARGUMENT', cache), '__EVENTVALIDATION': self.GetToken('__EVENTVALIDATION', cache), 'ctl00$cphRoblox$GroupStatusPane$MakePrimaryGroup': 'Make Primary'}, True)
		except:
			return False

	def InviteToClan(self, intID, intTarget):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			return True if 'true' in self.NetworkRequest('http://www.roblox.com/group/invite-to-clan', {'userIdToInvite': `intTarget`, 'groupId': `intID`, '__RequestVerificationToken': self.GetToken('VERIFICATION', cache)}, True, self.GetToken('CSRF', cache)) else False
		except:
			return False

	def CancelClanInvite(self, intID, intTarget):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			return True if 'true' in self.NetworkRequest('http://www.roblox.com/group/cancel-invitation', {'inviteeUserId': `intTarget`, 'groupId': `intID`, '__RequestVerificationToken': self.GetToken('VERIFICATION', cache)}, True, self.GetToken('CSRF', cache)) else False
		except:
			return False

	def AcceptClanInvite(self, intID, boolAccept):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			return True if 'true' in self.NetworkRequest('http://www.roblox.com/group/accept-decline-clan-invitation', {'isAccepting': `boolAccept`, 'groupId': `intID`, '__RequestVerificationToken': self.GetToken('VERIFICATION', cache)}, True, self.GetToken('CSRF', cache)) else False	
		except:
			return False

	def KickFromClan(self, intID, intTarget):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			return True if 'true' in self.NetworkRequest('http://www.roblox.com/group/kick-from-clan', {'userIdToKick': `intTarget`, 'groupId': `intID`, '__RequestVerificationToken': self.GetToken('VERIFICATION', cache)}, True, self.GetToken('CSRF', cache)) else False	
		except:
			return False

	def LeaveClan(self, intID):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Groups.aspx?gid=' + `intID`, None, True)

			return True if 'true' in self.NetworkRequest('http://www.roblox.com/group/leave-clan', {'groupId': `intID`, '__RequestVerificationToken': self.GetToken('VERIFICATION', cache)}, True, self.GetToken('CSRF', cache)) else False	
		except:
			return False

	#
	#	Asset API
	#

	def GetAsset(self, intID):
		try:
			return json.loads(self.NetworkRequest('http://api.roblox.com/Marketplace/ProductInfo?assetId=' + `intID`))
		except:
			return False

	def BuyAsset(self, intID, intCurrency):
		try:
			arrData = self.GetAsset(intID)
			if arrData['IsPublicDomain'] is False:
				expectedCurrency = 1 if intCurrency == 1 and arrData['PriceInRobux'] is not 'null' else 2
				expectedPrice = arrData['PriceInRobux'] if intCurrency == 1 and arrData['PriceInRobux'] is not 'null' else arrData['PriceInTickets']
				self.NetworkRequest('http://www.roblox.com/API/Item.ashx?rqtype=purchase&productID=' + arrData['ProductId'] + '&expectedCurrency=' + `expectedCurrency` + '&expectedPrice=' + `expectedPrice` + '&expectedSellerID=' + `arrData['Creator']['Id']`, {}, True, self.GetToken('CSRF'))
			else:
				self.NetworkRequest('http://www.roblox.com/API/Item.ashx?rqtype=purchase&productID=' + arrData['ProductId'] + '&expectedCurrency=1&expectedPrice=0&expectedSellerID=' + arrData['Creator']['Id'], {}, True, self.GetToken('CSRF'))
		except:
			return False

	def HasAsset(self, intUser, intID):
		try:
			return True if 'true' in self.NetworkRequest('http://api.roblox.com/Ownership/HasAsset?userId=' + `intUser` + '&assetId=' + `intID`) else False
		except:
			return False

	def UpdateAsset(self, intID, strName, srtDesc, boolComments, intGenre, boolForSale, intRobux = 0, intTickets = 0):
		try:
			cache = self.NetworkRequest('http://www.roblox.com/My/Item.aspx?ID=' + `intID`, None, True)

			if intRobux <= 0 or intTickets <= 0:
				self.NetworkRequest('http://www.roblox.com/My/Item.aspx?ID=' + `intID`, {'__EVENTTARGET': 'ctl00$cphRoblox$SubmitButtonTop', '__EVENTARGUMENT': '', '__VIEWSTATE': self.GetToken('VIEWSTATE', cache), '__EVENTVALIDATION': self.GetToken('EVENTVALIDATION', cache), 'ctl00$cphRoblox$NameTextBox': strName, 'ctl00$cphRoblox$DescriptionTextBox': srtDesc, 'ctl00$cphRoblox$EnableCommentsCheckBox': ('on' if boolComments == True else ''), 'GenreButtons2': self.GetGenreSetting(intGenre), 'ctl00$cphRoblox$actualGenreSelection': self.GetGenreSetting(intGenre), 'ctl00$cphRoblox$PublicDomainCheckBox': ('on' if boolForSale == True else '')}, True)
			else:
				self.NetworkRequest('http://www.roblox.com/My/Item.aspx?ID=' + `intID`, {'__EVENTTARGET': 'ctl00$cphRoblox$SubmitButtonTop', '__EVENTARGUMENT': '', '__VIEWSTATE': self.GetToken('VIEWSTATE', cache), '__EVENTVALIDATION': self.GetToken('EVENTVALIDATION', cache), 'ctl00$cphRoblox$NameTextBox': strName, 'ctl00$cphRoblox$DescriptionTextBox': srtDesc, 'ctl00$cphRoblox$EnableCommentsCheckBox': ('on' if boolComments == True else ''), 'GenreButtons2': self.GetGenreSetting(intGenre), 'ctl00$cphRoblox$actualGenreSelection': self.GetGenreSetting(intGenre), 'ctl00$cphRoblox$SellThisItemCheckBox': ('on' if boolForSale == True else ''), 'SellForRobux': ('on' if intRobux > 0 else ''), 'SellForTickets': 'on' if intTickets > 0 else None, 'RobuxPrice': `intRobux`, 'TicketsPrice': `intTickets`}, True)
		except:
			return False

	def ToggleFavoriteAsset(self, intID):
		try:
			return True if 'True' in self.NetworkRequest('http://www.roblox.com/favorite/toggle', {'assetId' : `intID`}, True) else False
		except:
			return False

	# NOTICE: this will only return true if the current user that is logged in has the asset favorited
	def IsAssetFavorited():
		try:
			soup = BeautifulSoup(self.NetworkRequest('http://www.roblox.com/games/' + `intID` + '/-'), 'html.parser')

			return True if len(soup.find_all('span', {'class' : 'rbx-icon-favorite favorited'})) > 0 else False
		except:
			return False

	def VoteAsset(self, intID, boolVote):
		try:
			self.NetworkRequest('http://www.roblox.com/voting/vote?assetId=' + `intID` + '&vote=' + `boolVote`, {}, True)
		except:
			return False

	#
	#	Misc API
	#

	def RedeemPromocode(self, strCode):
		try:
			return True if 'true' in self.NetworkRequest('http://www.roblox.com/promocodes/redeem?code=' + strCode, {}, True) else False
		except:
			return False

	#
	#	Chat API
	#

	currentConversation = None
	currentMessage = None
	currentMethod = None

	# Gets all the conversations that were ever started
	def GetConversations(self, intPage = 1, intSize = 9999):
		try:
			return json.loads(self.NetworkRequest('https://chat.roblox.com/v1.0/get-user-conversations?pageNumber=' + `intPage` + '&pageSize=' + `intSize`, None, True))
		except:
			return False

	# Gets the creator of the covnersation
	def GetInitiator(self):
		try:
			return self.currentConversation['InitiatorUser']['Id']
		except:
			return False

	# Gets all the particpants in a chat, it also returns the current user
	def GetParticipants(self):
		try:
			arrResult = []

			for Participant in self.currentConversation['ParticipantUsers']:
				arrResult.append(Participant['Id'])

			return arrResult
		except:
			return False

	# Returns the current's chat id
	def GetChatID(self):
		try:
			return self.currentConversation['Id']
		except:
			return False

	# Checks if the chat is a groupchat (aka party)
	def IsGroupChat(self):
		try:
			return self.currentConversation['IsGroupChat']
		except:
			return False

	def HasUnreadMessages(self):
		try:
			return self.currentConversation['HasUnreadMessages']
		except:
			return False

	def GetChatMessages(self, intConversation, intSize = 9999):
		try:
			return json.loads(self.NetworkRequest('https://chat.roblox.com/v1.0/get-messages?conversationId=' + `intConversation` + '&pageSize=' + `intSize`, None, True))
		except:
			return False

	def GetLastMessage(self, intConversation):
		try:
			return self.GetMessages(intConversation, 1)[0]
		except:
			return False

	def GetMessageContent(self):
		try:
			return self.currentMessage['Content']
		except:
			return False

	def GetMessageID(self):
		try:
			return self.currentMessage['Id']
		except:
			return False

	def IsMessageRead(self):
		try:
			return self.currentMessage['Read']
		except:
			return False	

	def GetSender(self):
		try:
			return self.currentMessage['SenderUserId']
		except:
			return False

	def GetDate(self):
		try:
			return self.currentMessage['Sent']
		except:
			return False

	def StartConversation(self, intID):
		try:
			return json.loads(self.NetworkRequest('https://chat.roblox.com/v1.0/start-one-to-one-conversation', {'participantUserID': `intID`}, True, self.GetToken('CSRF')))['Conversation']
		except:
			return False

	def IsSucces(self):
		try:
			return self.currentMethod['Succes']
		except:
			return False

	def SendChatMessage(self, intConversation, strMessage):
		try:
			return json.loads(self.NetworkRequest('https://chat.roblox.com/v1.0/send-message', {'conversationId': `intConversation`, 'message': strMessage}, True, self.GetToken('CSRF')))
		except:
			return False

	def GetSentID(self):
		try:
			return self.currentMethod['MessageId']
		except:
			return False

	def GetUnreadCount(self):
		try:
			return self.NetworkRequest('https://chat.roblox.com/v1.0/get-unread-conversation-count', None, True)
		except:
			return False

	def MarkAsRead(self, intConversation, intID):
		try:
			return json.loads(self.NetworkRequest('https://chat.roblox.com/v1.0/mark-as-read', {'conversationId': `intConversation`, 'endMessageId': `intID`}, True, self.GetToken('CSRF')))
		except:
			return False

	def AddToConversation(self, intConversation, arrIDs):
		try:
			return True if 'true' in self.NetworkRequest('https://chat.roblox.com/v1.0/add-to-conversation', {'conversationId': `intConversation`, 'participantUserIds': arrIDs}, True, self.GetToken('CSRF')) else False
		except:
			return False

	def RemoveFromConversation(self, intID):
		try:
			return True if 'true' in self.NetworkRequest('https://chat.roblox.com/v1.0/remove-from-conversation', {'conversationId': `intConversation`, 'participantUserIds': intID}, True, self.GetToken('CSRF')) else False
		except:
			return False

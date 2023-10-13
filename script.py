import pandas as pd
import requests
import pickle
from bs4 import BeautifulSoup

class scraper_class:
	class bayut:
		class buy:
			def get_all_adds_links(self):
				errors = []
				all_adds_links = []

				pages_urls = ["https://www.bayut.com/for-sale/property/uae/"]
				for i in range(2, 1667):
					pages_urls.append("https://www.bayut.com/for-sale/property/uae/page-{i}/")

				for e, url in enumerate(pages_urls):
					print(f'{e} | all_links: {len(all_adds_links)} | Errors: {len(errors)}')
					try:
						soup = BeautifulSoup(requests.get(url).text, "lxml")
						a = soup.select("article", {"class" : "ca2f5674"})
						for i in a:
							try:
								all_adds_links.append(i.find("a")['href'])
							except:
								errors.append(url)
					except:
						pass

				pickle.dump(all_adds_links, open("all_adds_link-bayut-buy.pkl", "wb"))

			def fetch_data_using_add_link(self):
				errors = []
				all_records_list = []

				all_adds_links = pickle.load(open("all_adds_link-bayut-buy.pkl", "rb"))

				for e, url in enumerate(all_adds_links):
					try:
						soup = BeautifulSoup(requests.get("https://www.bayut.com/for-sale/property/uae" + url).text, "lxml")
						a = [i.text for i in soup.find("ul", {"class" : "_033281ab"}).select("span", {"class" : "_3af7fa95"})]
						b = []
						for i in a:
							if not i.isnumeric():
								if not i in b:
									b.append(i)
							else:
								b.append(i)
						one_record_dict = dict(zip(b[::2], b[1:][::2]))
						one_record_dict["url"] = url
						all_records_list.append(one_record_dict)
					except:
						errors.append(url)
					print(e, end=", ")

				df = pd.DataFrame(all_records_list)

				df.to_pickle("df-bayut-buy.pkl")
				pickle.dump(errors, open("errors-bayut-buy.pkl", "rb"))
				pickle.dump(all_records_list, open("all_records_list-bayut-buy.pkl", "rb"))


		class rent:
			def get_all_adds_links(self):
				errors = []
				all_adds_links = []

				pages_urls = ["https://www.bayut.com/to-rent/property/uae/"]
				for i in range(2, 1934):
					pages_urls.append(f"https://www.bayut.com/to-rent/property/uae/page-{i}/")

				for e, url in enumerate(pages_urls):
					print(f'{e} | all_links: {len(all_adds_links)} | Errors: {len(errors)}')
					
					try:
						soup = BeautifulSoup(requests.get(url).text, "lxml")
						a = soup.find("ul", {"class" : "_357a9937"}).select("li", {"class" : "ef447dde"})
						for i in a:
							try:
								all_adds_links.append(i.find("div", {"class" : "_4041eb80"}).find("a")['href'])
							except:
								errors.append(url)
					except:
						pass
				pickle.dump(all_adds_links, open("all_adds_link-bayut-rent.pkl", "wb"))

			def fetch_data_using_add_link(self):

				errors = []
				all_records_list = []

				all_adds_links = pickle.load(open("all_adds_link-bayut-rent.pkl", "rb"))
				for e, url in enumerate(all_adds_links):
					print(e, end=", ")
					try:
						soup = BeautifulSoup(requests.get("https://www.bayut.com/for-sale/property/uae" + url).text, "lxml")
						a = [i.text for i in soup.find("ul", {"class" : "_033281ab"}).select("span", {"class" : "_3af7fa95"})]
						b = []
						for i in a:
							if not i.isnumeric():
								if not i in b:
									b.append(i)
							else:
								b.append(i)
						one_record_dict = dict(zip(b[::2], b[1:][::2]))
						all_records_list.append(one_record_dict)
					except:
						errors.append(url)

				df = pd.DataFrame(all_records_list)
				df.to_pickle("df.pkl")

				pickle.dump(errors, open("errors.pkl", "wb"))
				pickle.dump(all_records_list, open("all_records_list-bayut-rent.pkl", "wb"))


	def justproperty(self):
		all_data = []
		base_url = "https://www.justproperty.com"

		urls = [f"{base_url}/en/agents/"]
		for i in range(2, 98):
			urls.append(f"{base_url}/en/agents/?page={i}")

		for url in urls:
			soup = BeautifulSoup(requests.get(url).text, "lxml")
			a = soup.find("div", {"class" : "body"}).select("div", {"class" : "item"})
			for item in a:
				try:
					b = item.find("div", {"class" : "columns cols-4-12 cols-m-12-12 cols-t-4-12 company-contact-info"})
					c = b.find("div", {"class" : "buttons"}).a
					d = c.attrs

					hrefs = item.find("div", {"class" : "details-contact-info-links"}).select("a")
					dict_href_rent_and_sale = {}
					for i in hrefs:
						dict_href_rent_and_sale[i.text.split()[0].strip()] = base_url + i['href']

					company_id   = int(eval(c['data-stats'])['company_id'])
					phone_number = int(c['data-phone'].replace("'", ""))
					company_name = item.find("div", {"class" : "columns cols-6-12 cols-m-12-12 cols-t-8-12 company-info"}).find("h1").text.strip()
					company_url  = base_url + item.find("div", {"class" : "columns cols-6-12 cols-m-12-12 cols-t-8-12 company-info"}).find("h1").find("a")['href']
					soup_company = BeautifulSoup(requests.get(company_url).text, "lxml")
					soup_company.find("div", {"class" : "columns cols-4-12 cols-m-12-12 cols-t-4-12 company-contact-info"}).\
									find("div", {"class" : "address"}).text.strip()
					LatLng = str(soup_company)[str(soup_company).index("new google.maps.LatLng"): str(soup_company).index("new google.maps.LatLng")+70].replace("new google.maps.LatLng(", "")
					LatLng = [float(i.strip()) for i in LatLng[:LatLng.index(");")].split(",")]

					company_info_dict = {}
					company_info_dict['phone number'] = phone_number
					company_info_dict['company id']   = company_id
					company_info_dict['Rental link']  = dict_href_rent_and_sale['Rental']
					company_info_dict['Sales link']   = dict_href_rent_and_sale['Sales']
					company_info_dict['company name'] = company_name
					company_info_dict['company_url']  = company_url
					company_info_dict['LatLng']       = LatLng
					if not company_info_dict in all_data:
						all_data.append(company_info_dict)
				except:
					pass
		
		pd.DataFrame(all_data).to_csv("justproperty.csv", index=False)

	class property_finder:
		class buy:
			def get_all_adds_links(self):
				links_buy = []
				urls = ["https://www.propertyfinder.ae/en/buy/properties-for-sale.html?page=" + str(i) for i in range(1, 1635)]
				for url in urls:
					soup = BeautifulSoup(requests.get(url).text, "lxml")
					a = soup.find("div", {"data-qs" : "property-list"}).find("div", {"class" : "card-list card-list--property"})
					for i in a.select("div", {"class" : "card-list__item", "data-qs" : "cardlist"}):
						try:
							i.find("div", {"class" : "card__image card__image--property"}).text
							b = i.find("a")
							links_buy.append(b['href'])
						except:
							pass
					pickle.dump(links_buy, open("links-buy-property_finder.pkl", "wb"))
	
	
			def fetch_data_using_add_link(self):
				# all_records_list = []
				# errors = []

				# links_buy = pickle.load(open("links-buy-property_finder.pkl", "rb"))
				# links_buy = ["https://www.propertyfinder.ae" + i for i in links_buy]

				# for url in links_buy:
				#     try:
				#         values = []
				#         keys = []
				#         soup = BeautifulSoup(requests.get(url).text, "lxml")
				#         a = soup.find("div", {"class" : "facts__container"}).find("div", {"class", "facts__list"})
				#         for e, i in enumerate(a.find_all("div", {"class" : "facts__list-item"})):
				#             if e != 4:
				#                 keys.append(i.find("div", {"class" : "facts__label"}).text.strip())
				#         for e, i in enumerate(a.find_all("div", {"class" : "facts__content"})):
				#             if e != 3:
				#                 values.append(i.text.strip().replace("\n", "").replace("  ", ""))
						
				#         b = soup.find("div", {"class" : "amenities__list"})
				#         amenities = list(set([i.text.strip() for i in b.select("div", {"class" : "amenities__list-item"})]))
				#         str_amenities = "{"
				#         for i in amenities:
				#             str_amenities += i + ","
				#         str_amenities += "}"
				#         str_amenities = str_amenities.replace(",}", "}")
				#         price = soup.find("span", {"class" : "facts__content--price-value"}).text
				#         phone = int(''.join([i for i in str(soup)[str(soup).find("tel:"): str(soup).find("tel:")+20] if i.isnumeric() or i == "+"]))
						
				#         one_record_dict = dict(zip(keys, values))
				#         one_record_dict['url'] = url
				#         one_record_dict['amenities'] = str_amenities
				#         one_record_dict['price'] = price
				#         one_record_dict['phone'] = phone
				#         all_records_list.append(one_record_dict)
				#     except:
				#         errors.append(url)
			

				# df = pd.DataFrame(all_records_list)

				# df.to_pickle("df-roperty-finder.pkl")
				# pickle.dump(errors, open("errors-property-finder.pkl", "wb"))
				# pickle.dump(all_records_list, open("all_records_list-property-finder.pkl", "wb"))
			

				links_buy = pickle.load(open("links-buy-property_finder.pkl", "rb"))

				error_links = []
				list_of_all_properties = []
				base_url = "https://www.propertyfinder.ae"

				for ee, url in enumerate(links_buy):
					try:
						soup = BeautifulSoup(requests.get(base_url + url).text, "lxml")
						a = soup.find("div", {"class" : "property-page__facts-amenities"}).find("div", {"class" : "facts__list"})

						lst = []
						for e, i in enumerate(a.select("div", {"class" : "facts__list-item"})):
							if e in [1,3,10,11,13,14, 22, 23, 25, 26, 28, 29,31, 32]:
								lst.append(''.join(i.text.strip().splitlines()).replace("  ", ""))

						one_property_dict = dict(zip(lst[::2], lst[1:][::2]))
						one_property_dict['url'] = base_url + url
						list_of_all_properties.append(one_property_dict)
					except:
						error_links.append(ee)
					print(f"Link number: {ee}\t\tLenght of list: {len(list_of_all_properties)}\t\tErrors Qty: {len(error_links)}")

				df = pd.DataFrame(list_of_all_properties)

				pickle.dump(error_links, open("errors-buy-property_finder.pkl", "wb"))
				pickle.dump(list_of_all_properties, open("list_of_all_properties-buy-property_finder.pkl", "wb"))
				df.to_pickle("df-buy-property_finder")

		class rent:
			def get_all_adds_links(self):
				links_rent = []
				errors = []

				urls = ["https://www.propertyfinder.ae/en/rent/properties-for-rent.html?page=" + str(i) for i in range(1, 1866)]

				for e, url in enumerate(urls):
					soup = BeautifulSoup(requests.get(url).text, "lxml")
					try:
						a = soup.find("div", {"data-qs" : "property-list"}).find("div", {"class" : "card-list card-list--property"})
						for i in a.select("div", {"class" : "card-list__item", "data-qs" : "cardlist"}):
							try:
								i.find("div", {"class" : "card__image card__image--property"}).text
								b = i.find("a")
								links_rent.append(b['href'])
							except:
								pass
					except:
						errors.append(e)
						pass
					print(len(links_rent), end="|")
				pickle.dump(errors, open("errors-property-finder.pkl", 'wb'))
				pickle.dump(links_rent, open("links-rent-property-finder.pkl", "wb"))
				
			def fetch_data_using_add_link(self):

				links_rent = pickle.load(open("links-rent-property-finder.pkl", "rb"))
				base_url = "https://www.propertyfinder.ae"

				error_links = []
				list_of_all_properties = []

				for ee, url in enumerate(links_rent):
					try:
						soup = BeautifulSoup(requests.get(base_url + url).text, "lxml")
						a = soup.find("div", {"class" : "property-page__facts-amenities"}).find("div", {"class" : "facts__list"})

						lst = []
						for e, i in enumerate(a.select("div", {"class" : "facts__list-item"})):
							if e in [1,3,10,11,13,14, 22, 23, 25, 26, 28, 29,31, 32]:
								lst.append(''.join(i.text.strip().splitlines()).replace("  ", ""))

						one_property_dict = dict(zip(lst[::2], lst[1:][::2]))
						one_property_dict['url'] = base_url + url
						list_of_all_properties.append(one_property_dict)
					except:
						error_links.append(ee)

					print(f"Link number: {ee}\t\tLenght of list: {len(list_of_all_properties)}\t\tErrors Qty: {len(error_links)}")

				df = pd.DataFrame(list_of_all_properties)

				pickle.dump(error_links, open("errors-rent-property-finder.pkl", "wb"))
				pickle.dump(list_of_all_properties, open("list_of_all_properties-rent-property-finder.pkl", "wb"))
				pickle.dump(df, open("df-rent-property-finder.pkl", "wb"))



obj = scraper_class()

obj.bayut.buy().get_all_adds_links()
obj.bayut.buy().fetch_data_using_add_link()

obj.bayut.rent().get_all_adds_links()
obj.bayut.rent().fetch_data_using_add_link()

obj.justproperty()

obj.property_finder.buy().get_all_adds_links()
obj.property_finder.buy().fetch_data_using_add_link()

obj.property_finder.rent().get_all_adds_links()
obj.property_finder.rent().fetch_data_using_add_link()

#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Igor Hercowitz, Alê Borba"
__version__ = "v0.6.1"

from urllib import urlencode
from urllib2 import urlopen, URLError, HTTPError

# Valores válidos para filtro sort
SORT_VALUES = ['price', 'dprice', 'rate', 'drate', 'seller', 'dseller',
                'installment', 'dinstallment', 'numberofinstallments',
                'dnumberofinstallments', 'trustedStore']

# Volores válidos para medal
MEDAL_VALUES = ['all', 'diamond', 'gold', 'silver', 'bronze']

class Buscape():
    """
    Class for BuscaPé's API abstraction
    """

    def __init__(self, applicationID=None, country="BR"):
        if not applicationID:
            raise ValueError("User ID must be specified")

        self.applicationID = applicationID

        self.environment = 'bws'

        if country is None:
            self.country = "BR"
        else:
            self.country = country

    def __fetch_url(self, url=None):
        try:
            resp = urlopen(url)
            data = resp.read()
            return dict(code=resp.code, data=data)
        except HTTPError, e:
            if e.code == 401:
                if self.environment == 'bws':
                    raise HTTPError(url, e.code, "Your application is not "
                                    "approved yet", None, None)
                else:
                    raise HTTPError(url, e.code, "The request requires user "
                                    "authentication", None, None)
        except URLError, e:
            code_error = e.reason.errno

            if code_error == 11001:
                raise URLError("no connection avaliable")
            else:
                raise URLError(e)

    def __search(self, method=None, parameter=None):
        if self.environment != 'sandbox':
            self.environment = 'bws'

        req = "http://%s.buscape.com/service/%s/%s/%s/?%s" %\
              (self.environment, method, self.applicationID, self.country,
               parameter)

        try:
            ret = self.__fetch_url(url=req)
            return ret
        except HTTPError, e:
            raise e
        except URLError, e:
            raise e

    def __default_filter(self, format='XML', results=10, page=1, priceMin=None,
                         priceMax=None, sort=None, medal=None):
        '''
        Lista de produtos, lista de ofertas, lista de produtos populares,
        avaliação de usuários têm os mesmos parâmetros de filtro.
        Método para evitar repetição.
        '''
        if format.upper() not in ["XML", "JSON"]:
            raise ValueError("the return format must be XML or JSON")

        if results is not None:
            if not isinstance(results, int) or not (0 < results < 999):
                raise ValueError('results must be a integer between 1 and 999')

        if page is not None:
            if not isinstance(page, int) or not (0 < page < 999):
                raise ValueError('page must be a integer between 1 and 999')

        if priceMin is not None:
            try:
                priceMin = float(priceMin)
            except ValueError:
                raise AssertionError('priceMin must be a float')
            except TypeError:
                raise TypeError('priceMin must be a float')

            if priceMin < 0.0:
                raise ValueError('priceMin cannot be negative.')

        if priceMax is not None:
            try:
                priceMax = float(priceMax)
            except ValueError:
                raise AssertionError('priceMax must be a float')
            except TypeError:
                raise TypeError('priceMax must be a float')


            if priceMax < 0.0:
                raise ValueError('priceMax cannot be negative.')

        if priceMax is not None and priceMin is not None:
            if priceMax < priceMin:
                raise ValueError('priceMax must be greater then priceMin')

        if sort is not None:
            if sort not in SORT_VALUES:
                # TODO: Melhorar mensagem de erro, indicar valores
                # válidos
                raise ValueError('The value in the sort parameter is not '
                                 'valid')

        if medal is not None:
            if medal not in MEDAL_VALUES:
                # TODO: Melhorar mensagem de erro
                raise ValueError('The value in the medal parameter is not '
                                 'valid')

        params = {'format': format, 'results': results, 'page': page}

        if priceMin is not None:
            params['priceMin'] = priceMin

        if priceMax is not None:
            params['priceMax'] = priceMax

        if sort is not None:
            params['sort'] = sort

        if medal is not None:
            params['medal'] = None

        return params

    def _validate_categoryID(self, categoryID):
        if categoryID is not None:
            if not isinstance(categoryID, int):
                raise AssertionError('categoryID must be int')
            if categoryID < 0:
                raise ValueError('categoryID must be positive')

    def set_sandbox(self):
        """
        Define the environment test
        """
        self.environment = 'sandbox'

    def find_category_list(self, keyword=None, categoryID=None, format='XML'):
        """
        Método faz busca de categorias, permite que você exiba informações
        relativas às categorias. É possível obter categorias, produtos ou
        ofertas informando apenas um ID de categoria.
        """

        if not keyword and categoryID is None:
            raise ValueError("keyword or categoryID option must be specified")
        elif keyword and categoryID:
            raise ValueError("you must specify only keyword or categoryID. "
                             "Both values aren't accepted")

        self._validate_categoryID(categoryID)
        params = self.__default_filter(format=format)

        if keyword:
            params['keyword'] = keyword
        else:
            params['categoryId'] = categoryID

        parameter = urlencode(params)

        return self.__search(method='findCategoryList', parameter=parameter)

    def find_product_list(self, keyword=None, categoryID=None, format='XML',
                          lomadee=False, results=10, page=1, minPrice=None,
                          maxPrice=None, sort=None, medal=None):
        """
        Método permite que você busque uma lista de produtos únicos
        utilizando o id da categoria final ou um conjunto de palavras-chaves
        ou ambos.
        """
        if keyword is None and categoryID is None:
            raise ValueError("keyword or categoryID option must be specified")

        self._validate_categoryID(categoryID)
        params = self.__default_filter(format, results, page, minPrice,
                                  maxPrice, sort, medal)

        if keyword:
            params['keyword'] = keyword
        if categoryID:
            params['categoryId'] = categoryID

        if lomadee:
            method = "findProductList/lomadee"
        else:
            method = "findProductList"

        parameter = urlencode(params)

        return self.__search(method=method, parameter=parameter)

    def create_source_id(self, sourceName=None, publisherID=None, siteID=None,
                         campaignList=None, token=None, format='XML'):
        """
        Serviço utilizado somente na integração do Aplicativo com o Lomadee.
        Dentro do fluxo de integração, o aplicativo utiliza esse serviço
        para criar sourceId (código) para o Publisher que deseja utiliza-lo.
        Os parâmetros necessários neste serviço são informados pelo
        próprio Lomadee ao aplicativo.
        No ambiente de homologação sandbox, os valores dos parâmetros podem
        ser fictícios pois neste ambiente este serviço retornará sempre o
        mesmo sourceId para os testes do Developer.
        """

        params = self.__default_filter(format=format)

        if not sourceName:
            raise ValueError("sourceName option must be specified")

        if not publisherID:
            raise ValueError("publisherID option must be specified")

        if not siteID:
            raise ValueError("siteID option must be specified")

        if not token:
            raise ValueError("token option must be specified")

        params.update({'sourceName': sourceName, 'publisherId': publisherID,
                       'siteId': siteID, 'token': token})

        if campaignList:
            params['campaignList'] = campaignList

        parameter = urlencode(params)

        return self.__search(method='createSource/lomadee', parameter=parameter)


    def find_offer_list(self, categoryID=None, productID=None, barcode=None,
                        keyword=None, lomadee=False, format="XML",
                        results=10, page=1, priceMin=None, priceMax=None,
                        sort=None, medal=None):
        """
        Método permite que você busque uma lista de produtos únicos
        utilizando o id da categoria final ou um conjunto de palavras-chaves
        ou ambos.
        """
        self._validate_categoryID(categoryID)
        params = self.__default_filter(format, results, page, priceMin,
                                       priceMax, sort, medal)

        if lomadee:
            method = 'findOfferList/lomadee'
        else:
            method = 'findOfferList'

        if keyword is not None and categoryID is not None:
            params.update({'keyword': keyword, 'categoryId': categoryID})
        elif categoryID is not None:
            params['categoryId']  = categoryID
        elif productID is not None:
            params['productID'] = productID
        elif barcode is not None:
            params['barcode'] = barcode
        elif keyword is not None:
            params['keyword'] = keyword
        else:
            raise ValueError("One parameter must be especified")

        parameter = urlencode(params)

        return self.__search(method=method, parameter=parameter)


    def top_products(self, format="XML", results=10, page=1, priceMin=None,
                     priceMax=None, sort=None, medal=None):

        """
        Método que retorna os produtos mais populares do BuscaPé.
        """

        params = self.__default_filter(format, results, page, priceMin,
                                       priceMax, sort, medal)
        method = "topProducts"

        parameter = urlencode(params)

        return self.__search(method=method, parameter=parameter)

    def view_product_details(self, productID=None, format="XML"):
        """
        Método retorna os detalhes técnicos de um determinado produto.
        """
        params = self.__default_filter(format=format)

        if not productID:
            raise ValueError('productID option must be specified')

        method = "viewProductDetails"

        parameter = urlencode(params)

        return self.__search(method=method, parameter=parameter)

    def view_seller_details(self, sellerID=None, format="XML"):
        """
        Método que retorna os detalhes de uma loja ou empresa como:
        endereços, telefones de contato e etc.
        """

        if format.upper() not in ["XML", "JSON"]:
            raise ValueError("the return format must be XML or JSON")

        if not sellerID:
            raise ValueError("sellerID option must be specified")

        method = "viewSellerDetails"

        parameter = "sellerId=%s&format=%s" % (sellerID, format)

        ret = self.__search(method=method, parameter=parameter)

        return ret

    def view_user_ratings(self, productID=None, format="XML"):
        """
        Método que retorna as avaliações dos usuários sobre um determinado
        produto.
        """

        if format.upper() not in ["XML", "JSON"]:
            raise ValueError("the return format must be XML or JSON")

        if not productID:
            raise ValueError('productID option must be specified')

        method = "viewUserRatings"

        parameter = "productId=%s&format=%s" % (productID, format)

        ret = self.__search(method=method, parameter=parameter)

        return ret

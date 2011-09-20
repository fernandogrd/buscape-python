# -*- coding: utf-8 -*-
import unittest
import json
from urllib2 import URLError, HTTPError
import sys

sys.path.insert(0, '..')
from buscape import Buscape


class BuscapeTest(unittest.TestCase):
    def setUp(self):
        self.applicationID = '2b613573535a6d324874493d'
        self.b = Buscape(applicationID=self.applicationID)
        self.b.set_sandbox()

    def _get_code(self, resp):
        json_resp = json.loads(resp['data'])
        return json_resp['details']['code']

    def test_set_default_format(self):
        buscape = Buscape(self.applicationID)
        self.assertEqual(buscape.format, 'XML')
        buscape.set_default_format('json')
        self.assertEqual(buscape.format, 'json')

    def assertRaisesMessage(self, excClass, message, callableObj, *args,
                            **kwargs):
        try:
            callableObj(*args, **kwargs)
        except excClass, e:

            if excClass == URLError:
                reason = e.reason
            elif excClass == HTTPError:
                reason = e.msg
            else:
                reason = e.message

            if message is not None and reason == message:
                return True
            else:
                raise (self.failureException, "\nMessage expected: %s \nMessag"
                       "e raised: %s" % (message, reason))
        else:
            if hasattr(excClass, '__name__'):
                excName = excClass.__name__
            else:
                excName = str(excClass)
            raise self.failureException, "%s not raised" % excName

    """
    Tests for method assertRaisesMessage.
    """
    def test_assertRaisesMessage(self):
        def _raise(e):
            raise e
        self.assertTrue(
            self.assertRaisesMessage(
                Exception,
                'Error',
                _raise,
                Exception('Error'),
            )
        )

        self.assertRaises(
            Exception,
            self.assertRaisesMessage,
            Exception,
            _raise,
            Exception('Error'),
        )

        self.assertRaises(self.failureException,
            self.assertRaisesMessage,
            Exception,
            'Not correct',
            _raise,
            Exception('Error'),
        )


class BuscapeFastTest(BuscapeTest):

    def test_applicationid_cannot_be_none(self):
        self.assertRaisesMessage(
            ValueError,
            'User ID must be specified',
            Buscape,
        )

    def test_applicationid_cannot_be_blank(self):
        self.assertRaisesMessage(
            ValueError,
            'User ID must be specified',
            Buscape,
            applicationID='',
    )

    def test_validate_categoryID(self):
        self.assertRaisesMessage(
            AssertionError,
            'categoryID must be int',
            self.b._validate_categoryID,
            'teste',
        )

        self.assertRaisesMessage(
            ValueError,
            'categoryID must be positive',
            self.b._validate_categoryID,
            -20,
        )

        self.assertEqual(self.b._validate_categoryID(10), None)

    def test_default_filter(self):
        default_filter = self.b._Buscape__default_filter
        # format
        self.assertRaisesMessage(
            ValueError,
            'the return format must be XML or JSON',
            default_filter,
            format='',
        )

        # results
        self.assertRaisesMessage(
            ValueError,
            'results must be a integer between 1 and 999',
            default_filter,
            results='',
        )

        self.assertRaisesMessage(
            ValueError,
            'results must be a integer between 1 and 999',
            default_filter,
            results=1000,
        )

        # page
        self.assertRaisesMessage(
            ValueError,
            'page must be a integer between 1 and 999',
            default_filter,
            page=1000,
        )

        self.assertRaisesMessage(
            ValueError,
            'page must be a integer between 1 and 999',
            default_filter,
            page='',
        )

        # priceMin
        self.assertRaisesMessage(
            AssertionError,
            'priceMin must be a float',
            default_filter,
            priceMin='',
        )

        self.assertRaisesMessage(
            TypeError,
            'priceMin must be a float',
            default_filter,
            priceMin={},
        )

        self.assertRaisesMessage(
            ValueError,
            'priceMin cannot be negative.',
            default_filter,
            priceMin=-0.1,
        )

        # priceMax

        self.assertRaisesMessage(
            AssertionError,
            'priceMax must be a float',
            default_filter,
            priceMax='',
        )

        self.assertRaisesMessage(
            TypeError,
            'priceMax must be a float',
            default_filter,
            priceMax={},
        )

        self.assertRaisesMessage(
            ValueError,
            'priceMax cannot be negative.',
            default_filter,
            priceMax=-0.1,
        )

        self.assertRaisesMessage(
            ValueError,
            'priceMax must be greater then priceMin',
            default_filter,
            priceMin=1, priceMax=0.9,
        )

        # Sort
        self.assertRaisesMessage(
            ValueError,
            'The value in the sort parameter is not valid',
            default_filter,
            sort='reverse',
        )

        # Medal
        self.assertRaisesMessage(
            ValueError,
            'The value in the medal parameter is not valid',
            default_filter,
            medal='stone',
        )

        # Teste retorno válido
        self.assertEqual(
            default_filter(
                format='json', results=22, page=2, priceMin=1.0, priceMax=20.0,
                sort='price', medal='gold',
            ),
            {'sort': 'price', 'format': 'json', 'results': 22, 'page': 2,
            'priceMax': 20.0, 'medal': 'gold', 'priceMin': 1.0},
        )

    def test_find_category_parameters_must_be_int(self):
        self.assertRaisesMessage(
            ValueError,
            'keyword or categoryID option must be specified',
            self.b.find_category_list,
        )

        self.assertRaisesMessage(
            ValueError,
            'keyword or categoryID option must be specified',
            self.b.find_category_list,
            keyword='',
        )

    def test_find_category_both_parameters_are_not_accepted(self):
        self.assertRaisesMessage(
            ValueError,
            'you must specify only keyword or categoryID. Both values aren\'t'
            ' accepted',
            self.b.find_category_list,
            keyword='xxx', categoryID=999,
        )

    def test_find_product_parameters_must_exists(self):
        self.assertRaisesMessage(
            ValueError,
            'keyword or categoryID option must be specified',
            self.b.find_product_list,
        )

        self.assertRaisesMessage(
            AssertionError,
            'categoryID must be int',
            self.b.find_product_list,
            keyword='', categoryID='',
        )

        self.assertRaisesMessage(
            ValueError,
            'categoryID must be positive',
            self.b.find_product_list,
            categoryID=-1,
        )

    def test_create_source_id(self):
        # sourceName
        self.assertRaisesMessage(
            ValueError,
            'sourceName option must be specified',
            self.b.create_source_id,
        )

        # publisherID
        self.assertRaisesMessage(
            ValueError,
            'publisherID option must be specified',
            self.b.create_source_id, sourceName='xxx',
        )

        # publisherID
        self.assertRaisesMessage(
            ValueError,
            'publisherID must be int',
            self.b.create_source_id,
            sourceName='xxx', publisherID='xx',
        )

        # siteID
        self.assertRaisesMessage(
            ValueError,
            'siteID option must be specified',
            self.b.create_source_id,
            sourceName='xxx', publisherID=10,
        )

        self.assertRaisesMessage(
            ValueError,
            'siteID must be int',
            self.b.create_source_id,
            sourceName='xxx',
            publisherID=10, siteID='xx',
        )

        # token
        self.assertRaisesMessage(
            ValueError,
            'token option must be specified',
            self.b.create_source_id,
            sourceName='xxx', publisherID=10, siteID=10,
        )

    def test_find_offer_list_at_least_one_parameter_must_be_specified(self):
        self.assertRaisesMessage(
            ValueError,
            'One parameter must be especified',
            self.b.find_offer_list,
        )

    def test_view_product_details_productID_must_be_valid(self):
        self.assertRaisesMessage(
            ValueError,
            'productID option must be specified',
            self.b.view_product_details,
        )


    def test_view_seller_details(self):
        self.assertRaisesMessage(
            ValueError,
            'sellerID option must be specified',
            self.b.view_seller_details,
        )

        self.assertRaisesMessage(
            AssertionError,
            'sellerID must be int',
            self.b.view_seller_details,
            sellerID='k',
        )

    def test_view_user_ratings_productID_must_be_valid(self):
        self.assertRaisesMessage(
            ValueError,
            'productID option must be specified',
            self.b.view_user_ratings,
        )

        self.assertRaisesMessage(
            AssertionError,
            'productID must be int',
            self.b.view_user_ratings,
            productID='y',
        )


class BuscapeRequestTest(BuscapeTest):
    def setUp(self):
        super(BuscapeRequestTest, self).setUp()
        self.b.set_default_format('json')

    def test_application_has_not_been_approved(self):
        app = Buscape(applicationID=self.applicationID)

        self.assertRaisesMessage(
            HTTPError,
            'Your application is not approved yet',
            app.find_category_list, keyword='xxx',
        )

    def test_application_with_wrong_applicationID_and_country_None(self):
        app = Buscape(applicationID='xpto', country=None)
        app.set_sandbox()

        self.assertRaisesMessage(
            HTTPError,
            'The request requires user authentication',
            app.find_category_list,
            keyword='xxx',
        )

    def test_find_category_by_keyword(self):
        resp = self.b.find_category_list(keyword='LG')
        code = self._get_code(resp)
        self.assertEquals(code, 0)

        data = self.b.find_category_list(keyword='LG')['data']
        self.assertTrue(data is not None)

    def test_find_category_by_categoryId(self):
        resp = self.b.find_category_list(categoryID=0)
        code = self._get_code(resp)
        self.assertEquals(code, 0)

        data = self.b.find_category_list(categoryID=0)['data']
        self.assertTrue(data is not None)

    def test_view_user_ratings(self):
        resp = self.b.view_user_ratings(productID=10)
        code = self._get_code(resp)
        self.assertEquals(code, 0)

    def test_view_seller_details(self):
        resp = self.b.view_seller_details(sellerID=10)
        code = self._get_code(resp)
        self.assertEquals(code, 0)

    def test_view_product_details(self):
        # Produto Inválido
        resp = self.b.view_product_details(productID='y')
        code = self._get_code(resp)
        self.assertEquals(code, 101)

        # Produto Válido
        resp = self.b.view_product_details(productID='10')
        code = self._get_code(resp)
        self.assertEquals(code, 0)

    def test_top_products(self):
        resp = self.b.top_products()
        code = self._get_code(resp)
        self.assertEquals(code, 0)

    def test_find_offer_list(self):
        # barcode
        offer_list = self.b.find_offer_list(
            barcode='1234', sort='price', medal='gold',
        )

        code = self._get_code(offer_list)
        self.assertEquals(code, 0)

        # productID
        offer_list = self.b.find_offer_list(
            productID='1234', sort='price', medal='gold',
        )

        code = self._get_code(offer_list)
        self.assertEquals(code, 0)

        # lomadee
        offer_list = self.b.find_offer_list(
            keyword='xpto', lomadee=True, sort='price', medal='gold',
        )
        code = self._get_code(offer_list)

        self.assertEquals(code, 0)

        # All params
        offer_list = self.b.find_offer_list(
            keyword='xpto', lomadee=True, results=10, page=1, priceMin=0.1,
            priceMax=10.00, sort='price', medal='gold',
        )

        code = self._get_code(offer_list)
        self.assertEquals(code, 0)

        # keyword
        offer_list = self.b.find_offer_list(
            keyword='xpto', sort='price', medal='gold',
        )

        code = self._get_code(offer_list)
        self.assertEquals(code, 0)

        # categodyId
        offer_list = self.b.find_offer_list(
            categoryID=0, sort='price', medal='gold',
        )

        code = self._get_code(offer_list)
        self.assertEquals(code, 0)

        offer_list = self.b.find_offer_list(
            keyword='xpto', categoryID=0, sort='price', medal='gold',
        )

        code = self._get_code(offer_list)
        self.assertEquals(code, 0)

    def test_create_source_id_use(self):
        source_id = self.b.create_source_id(
            sourceName='xxx',
            publisherID=10,
            siteID=10,
            token='ghi',
            campaignList='1,2',
        )

        code = self._get_code(source_id)
        self.assertEquals(code, 0)

        # no campaignList
        source_id = self.b.create_source_id(
            sourceName='xxx', publisherID=10, siteID=10, token='ghi',
        )

        code = self._get_code(source_id)
        self.assertEquals(code, 0)

    def test_find_product_setting_maxPrice_must_return_200(self):
        find_product = self.b.find_product_list(
            keyword='celular', maxPrice=1200.50,
        )

        code = find_product['code']
        self.assertEquals(code, 200)

    def test_find_product_setting_minPrice_and_maxPrice_must_return_200(self):
        find_product = self.b.find_product_list(
            keyword='celular', minPrice=344.90, maxPrice=1200.50,
        )

        code = find_product['code']
        self.assertEquals(code, 200)

    def test_find_product_using_lomadee_must_return_200(self):
        find_product = self.b.find_product_list(
            keyword='celular', lomadee=True,
        )

        code = find_product['code']
        self.assertEquals(code, 200)

    def test_find_product_setting_all_variables(self):
        find_product = self.b.find_product_list(
            keyword='celular', categoryID=0, format='json', page=3, results=20,
            minPrice=344.90, maxPrice=1200.50,
        )

        code = find_product['code']
        self.assertEquals(code, 200)

    def test_find_product_setting_minPrice_must_return_200(self):
        find_product = self.b.find_product_list(
            keyword='celular', minPrice=200,
        )

        code = find_product['code']
        self.assertEquals(code, 200)

    def test_find_product_only_keyword_parameter_must_return_data(self):
        data = self.b.find_product_list(keyword='celular')['data']
        self.assertTrue(data is not None)

    def test_find_product_only_categoryid_parameter_must_return_200(self):
        code = self.b.find_product_list(categoryID=0)['code']
        self.assertEquals(code, 200)

    def test_find_product_only_categoryid_parameter_must_return_data(self):
        data = self.b.find_product_list(categoryID=0)['data']
        self.assertTrue(data is not None)

    def test_find_product_both_keywork_and_categoryid_must_return_200(self):
        find_product = self.b.find_product_list(
            keyword='celular', categoryID=0,
        )

        code = find_product['code']
        self.assertTrue(code, 200)

    def test_find_product_both_keywork_and_categoryid_must_return_data(self):
        find_product = self.b.find_product_list(
            keyword='celular', categoryID=0,
        )

        data = find_product['data']
        self.assertTrue(data is not None)

    def test_find_product_format_must_be_case_insensitive(self):
        code = self.b.find_product_list(categoryID=0, format='json')['code']
        self.assertEquals(code, 200)

    def test_find_product_results_must_be_between_1_and_999(self):
        code = self.b.find_product_list(categoryID=0, results=20)['code']
        self.assertEquals(code, 200)

    def test_find_product_page_must_be_between_1_and_999(self):
        code = self.b.find_product_list(categoryID=0, page=20)['code']
        self.assertEquals(code, 200)

    def test_find_product_only_keyword_parameter_must_return_200(self):
        code = self.b.find_product_list(keyword='celular')['code']
        self.assertEquals(code, 200)

    def test_find_category_parameter_format_must_be_case_insensitive(self):
        code = self.b.find_category_list(categoryID=0, format='json')['code']
        self.assertEquals(code, 200)


def suite_fast():
    return unittest.makeSuite(BuscapeFastTest, 'test')


def suite_request():
    return unittest.makeSuite(BuscapeRequestTest, 'test')

if __name__ == '__main__':
    unittest.main()

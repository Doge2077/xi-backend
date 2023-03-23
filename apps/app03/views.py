from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class category(APIView):
    def get(self, request):
        t = [
            {
                'cat_a_title': '第一卷',
                'cat_a_id': 1,
                'cat_a_info': [
                    {
                        'cat_b_title': '第一章',
                        'cat_b_id': 1,
                        'cat_b_info': [
                            {
                                'cat_c_title': '第一节',
                                'cat_c_id': 1,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 1,
                                        'cat_d_info': '第一卷第一章第一节.'
                                    }
                                ]
                            },
                            {
                                'cat_c_title': '第二节',
                                'cat_c_id': 2,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 2,
                                        'cat_d_info': '第一卷第一章第二节.'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'cat_b_title': '第二章',
                        'cat_b_id': 2,
                        'cat_b_info': [
                            {
                                'cat_c_title': '第一节',
                                'cat_c_id': 1,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 1,
                                        'cat_d_info': '第一卷第二章第一节'
                                    }
                                ]
                            },
                            {
                                'cat_c_title': '第二节',
                                'cat_c_id': 2,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 2,
                                        'cat_d_info': '第一卷第二章第二节'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'cat_a_title': '第二卷',
                'cat_a_id': 2,
                'cat_a_info': [
                    {
                        'cat_b_title': '第一章',
                        'cat_b_id': 1,
                        'cat_b_info': [
                            {
                                'cat_c_title': '第一节',
                                'cat_c_id': 1,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 1,
                                        'cat_d_info': '第二卷第一章第一节.'
                                    }
                                ]
                            },
                            {
                                'cat_c_title': '第二节',
                                'cat_c_id': 2,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 2,
                                        'cat_d_info': '第二卷第一章第二节'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'cat_b_title': '第二章',
                        'cat_b_id': 2,
                        'cat_b_info': [
                            {
                                'cat_c_title': '第一节',
                                'cat_c_id': 1,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 1,
                                        'cat_d_info': '第二卷第二章第一节'
                                    }
                                ]
                            },
                            {
                                'cat_c_title': '第二节',
                                'cat_c_id': 2,
                                'cat_c_info': [
                                    {
                                        'cat_d_title': '标题',
                                        'cat_d_id': 2,
                                        'cat_d_info': '第二卷第二章第二节'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        # t = [
        #     {
        #         'aa': 'aaaaa',
        #         'bb': [
        #             {
        #                 'ccc': 'ccc',
        #                 'ddd': [
        #                     {
        #                         'eee': 'eee'
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # ]
        return Response(t)
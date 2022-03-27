from flask import request, render_template, redirect, url_for, jsonify

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CityDAO import CityDAO
from project.com.vo.AreaVO import AreaVO


@app.route('/admin/loadArea', methods=['GET'])
def adminLoadArea():
    try:
        if adminLoginSession() == 'admin':
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            return render_template('admin/addArea.html', cityVOList=cityVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/insertArea', methods=['POST'])
def adminInsertArea():
    try:
        if adminLoginSession() == 'admin':
            areaName = request.form['areaName']
            areaPincode = request.form['areaPincode']
            area_CityId = request.form['area_CityId']

            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaVO.areaName = areaName
            areaVO.areaPincode = areaPincode
            areaVO.area_CityId = area_CityId

            areaDAO.insertArea(areaVO)

            return redirect(url_for('adminViewArea'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewArea', methods=['GET'])
def adminViewArea():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            return render_template('admin/viewArea.html', areaVOList=areaVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteArea', methods=['GET'])
def adminDeleteArea():
    try:
        if adminLoginSession() == 'admin':
            areaDAO = AreaDAO()

            areaId = request.args.get('areaId')

            areaDAO.deleteArea(areaId)

            return redirect(url_for('adminViewArea'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editArea', methods=['GET'])
def adminEditArea():
    try:
        if adminLoginSession() == 'admin':
            areaVO = AreaVO()

            areaDAO = AreaDAO()

            cityDAO = CityDAO()

            areaId = request.args.get('areaId')
            cityName = request.args.get('cityName')

            areaVO.areaId = areaId

            areaVOList = areaDAO.editArea(areaVO)

            cityVOList = cityDAO.viewCity()

            print(">>>>>>>>>>>>>>>>>>>>>>>>>>cityname>>>>>>>>>.", cityName)

            return render_template('admin/editArea.html', cityVOList=cityVOList, areaVOList=areaVOList,
                                   cityName=cityName)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/updateArea', methods=['POST'])
def adminUpdateArea():
    try:
        if adminLoginSession() == 'admin':

            areaName = request.form['areaName']
            areaPincode = request.form['areaPincode']
            area_CityId = request.form['area_CityId']
            areaId = request.form['areaId']

            areaVO = AreaVO()
            areaDAO = AreaDAO()

            areaVO.areaId = areaId
            areaVO.areaName = areaName
            areaVO.areaPincode = areaPincode
            areaVO.area_CityId = area_CityId

            areaDAO.updateArea(areaVO)

            return redirect(url_for('adminViewArea'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxArea')
def adminAjaxArea():
    areaVO = AreaVO()
    areaDAO = AreaDAO()

    area_CityId = request.args.get('cityId')

    areaVO.area_CityId = area_CityId

    ajaxProductAreaList = areaDAO.ajaxAreaProduct(areaVO)

    print(">>>>>>>>>>>ajaxProductAreaList>>>>>>>>>>", ajaxProductAreaList)

    ajaxAreaJson = [i.as_dict() for i in ajaxProductAreaList]

    print(">>>>>>>>>>>ajaxAreaJson>>>>>>>>>>", ajaxAreaJson)

    return jsonify(ajaxAreaJson)

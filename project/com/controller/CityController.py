from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.CityDAO import CityDAO
from project.com.vo.CityVO import CityVO


@app.route('/admin/loadCity')
def adminLoadCity():
    try:

        if adminLoginSession() == 'admin':
            return render_template('admin/addCity.html')

        else:
            return adminLogoutSession()


    except Exception as ex:
        print(ex)


@app.route('/admin/insertCity', methods=['POST'])
def adminInsertCity():
    try:
        if adminLoginSession() == 'admin':
            cityName = request.form['cityName']
            cityDescription = request.form['cityDescription']
            print(cityDescription)

            cityVO = CityVO()
            cityDAO = CityDAO()

            cityVO.cityName = cityName
            cityVO.cityDescription = cityDescription

            cityDAO.insertCity(cityVO)

            return redirect(url_for('adminViewCity'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewCity', methods=['GET'])
def adminViewCity():
    try:
        if adminLoginSession() == 'admin':
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            print("__________________", cityVOList)
            return render_template('admin/viewCity.html', cityVOList=cityVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCity', methods=['GET'])
def adminDeleteCity():
    try:
        if adminLoginSession() == 'admin':
            cityVO = CityVO()
            cityDAO = CityDAO()

            cityId = request.args.get('cityId')

            cityVO.cityId = cityId
            cityDAO.deleteCity(cityVO)

            return redirect(url_for('adminViewCity'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editCity', methods=['GET'])
def adminEditCity():
    try:
        if adminLoginSession() == 'admin':
            cityVO = CityVO()

            cityDAO = CityDAO()

            cityId = request.args.get('cityId')

            cityVO.cityId = cityId

            cityVOList = cityDAO.editCity(cityVO)

            print("=======cityVOList=======", cityVOList)

            print("=======type of cityVOList=======", type(cityVOList))

            return render_template('admin/editCity.html', cityVOList=cityVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/updateCity', methods=['POST'])
def adminUpdateCity():
    try:
        if adminLoginSession() == 'admin':
            cityId = request.form['cityId']
            cityName = request.form['cityName']
            cityDescription = request.form['cityDescription']

            cityVO = CityVO()
            cityDAO = CityDAO()

            cityVO.cityId = cityId
            cityVO.cityName = cityName
            cityVO.cityDescription = cityDescription

            cityDAO.updateCity(cityVO)

            return redirect(url_for('adminViewCity'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

# from website import create_app

# app= create_app()

# if __name__ == '__main__':
#     app.run(port=8080, debug=True)


from website import create_app

app = create_app()
# if __name__ == '__main__':
#   app.run(host ='192.168.56.1', port=7249, debug=True)


if __name__ == '__main__':
    app.run(debug=True)


 

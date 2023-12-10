from flask import jsonify , request
from app.utils.classToDict import classToDict , classToArrayOfDicts
from app.utils.validateFile import allowed_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime

def createRecipeRoute(db, Recipes , Ingrediants , user ):
    try:
        data = request.form.to_dict()
        filename = ""
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            alwd , ext =  allowed_file(filename) 
            if not alwd:
                return jsonify({'success': False, 'message': 'file type not allowed'}) , 400 
            filename = filename + datetime.now().strftime("%Y_%m_%d %H-%M-%S") + "." + ext
            file.save(os.path.join("static", filename ))
        
        recipe = Recipes(name=data['name'] , description=data['description'], added_by=user.id, image=filename, time=(data['time'].lower() if 'time' in data else '' ))
        
        db.session.add(recipe)
        recipeDict = classToDict(recipe)
        db.session.commit()
        
        if 'ingrediants[]'  in data:
                
            ingredients = request.form.getlist("ingrediants[]")
            newIngrediants = db.session.query(Ingrediants).filter(Ingrediants.name.in_(ingredients)).all()
            for newIng in newIngrediants:
                if newIng.name in ingredients:
                    ingredients.remove(newIng.name)
            
            for element in ingredients:
                newIngrediant = Ingrediants(name=element)
                newIngrediants.append(newIngrediant)
            db.session.add_all(newIngrediants)
            db.session.commit()

            recipe.ingrediants.extend(newIngrediants)
            db.session.commit()
            
            recipeDict['id'] = recipe.id
            recipeDict['ingrediants'] = classToArrayOfDicts(newIngrediants)
        return jsonify({'recipe': recipeDict , 'success' : True}) , 201
    except Exception as e:
        print(f"error creating recipe:\n error type: {type(e)}\n error: {e}")
        return jsonify({'success': False , 'message': "there was an error creating recipe, try again later"}) , 500
    
def getAllRecipiesRoute(db , Recipes):
    try:
        query = request.args.get("q")
        time = request.args.get("time")
        recipes = db.session.query(Recipes).filter(Recipes.name.like(f"%{query}%" )if (query != None) else True ).filter(Recipes.time == time.lower(    ) if (time != None) else True ).all()
        if len(recipes) == 0 :
            return jsonify({'success': False , 'message': "no recipes found"}) , 404
        recipesDict = classToArrayOfDicts(recipes)
        for i, recipe in enumerate(recipes):
            recipesDict[i]['ingrediants'] = (classToArrayOfDicts(recipe.ingrediants))
            pass
        return jsonify({'success': True , 'recipes': recipesDict }) , 200
    except Exception as e:
        print(f"error getting all recipes:\n error type: {type(e)}\n error: {e}")
        return jsonify({'success': False , 'message': "there was an error getting all recipes, try again later"}) , 500

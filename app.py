from flask import Flask, render_template, request, redirect
import csv
import stripe 
import re

stripe.api_key = 'YOUR STRIPE KEY'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/donation", methods=['GET', 'POST'])
def donation():
    if request.method == 'GET':
        return render_template("donation.html")
    else:
        first_name = request.form.get('first-name', '')
        last_name = request.form.get('last-name', '')
        street = request.form.get('street', '')
        phone = request.form.get('phone', '')
        amount = request.form.get('donation_value', '') 

        if '.' in amount:
            amount = amount.replace('.', '')
            if len(amount) == 2:
                amount = ''.join((amount, '0'))
        elif len(amount) > 2: 
            pass
        else:
            amount = ''.join((amount, '00'))
                
        errors: str = error_handling(first_name, last_name, street, phone, amount)
        if errors:
            return render_template('error.html', errors=errors)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'unit_amount': amount,
                        'product_data': {
                            'name': 'Donation'
                        }
                    },
                    'quantity': 1,
                }],
                
                mode='payment',
                success_url='http://127.0.0.1:5000/success', 
                cancel_url='http://127.0.0.1:5000/error',
            )
        except Exception as e:
            return render_template('error.html', message=e)

        with open('.\static\donations.csv', 'a', newline='') as csvfile:
            fieldnames = ['Primeiro nome', 'Sobrenome', 'Rua', 'Telefone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writerow({'Primeiro nome': first_name, 'Sobrenome': last_name, 'Rua': street, 'Telefone': phone})
        
        return redirect(checkout_session.url, code=303)

def error_handling(first_name: str, last_name: str, street: str, phone: str, amount: str) -> list[str]:
    errors = []

    if not first_name or not last_name:
        errors.append('Seu nome não pode estar vazio')
    if not first_name.isalpha() or not last_name.isalpha():
        errors.append('Seu nome deve ter apenas letras') 
    if not street:
        errors.append('Por favor nos informe seu endereço')
    
    pattern = r'^\d{2} (\d{4} \d{4}|\d{5}-\d{4})$'    
    if not re.match(pattern, phone):  
        errors.append('Seu telefone deve conter 9 dígitos e DDD')
    if not amount.isdigit():
        errors.append('Sua doação deve ser um valor numérico')
    if len(amount) <= 3 and amount < '300':
        errors.append('A doção mínima é de 3 reais')
    return errors

@app.route("/error")
def cancel():
    return render_template('error.html')

@app.route("/success")
def success():
    return render_template('thanks.html')
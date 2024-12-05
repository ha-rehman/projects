from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from register.models import UserExtension
from .models import TransactionHistory
from register.currency_conversion import get_exchange_rate


def __get_bool(my_str):
    if my_str.lower() == 'false':
        return False
    else:
        return True


def __verify_user(request, type, validate_recipient):
    try:
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        if user.id != request.user.id:
            validate_recipient = True
        else:
            label = "Transfer" if type == TransactionHistory.transfer else "Request"
            messages.error(request, f"{label} of payment to own account is not allowed!")
    except User.DoesNotExist:
        messages.error(request, "User Not Exists!")
    finally:
        return validate_recipient, username


def __make_transaction(request, type, validate_recipient):
    username = request.POST.get('username')
    amount = float(request.POST['amount'])
    base_amount = amount

    from_to = User.objects.get(id=request.user.id)
    from_to_account_details = UserExtension.objects.get(user=from_to)
    recipient_user = User.objects.get(username=username)
    recipient_account_details = UserExtension.objects.get(user=recipient_user)

    if from_to_account_details.balance >= amount or type == TransactionHistory.request:
        # save transaction
        mode = TransactionHistory.transfer if type == TransactionHistory.transfer else TransactionHistory.request
        status = TransactionHistory.completed if type == TransactionHistory.transfer else TransactionHistory.pending
        TransactionHistory.objects.create(sender=from_to, receiver=recipient_user, amount=amount, mode=mode,
                                          currency=from_to_account_details.currency, status=status)

        if type == TransactionHistory.transfer:
            # deduct balance from sender account
            from_to_account_details.balance -= amount
            from_to_account_details.save()

            # add balance in receiver account
            if from_to_account_details.currency != recipient_account_details.currency:
                rate, amount = get_exchange_rate(from_to_account_details.currency,
                                                 recipient_account_details.currency, amount)

            recipient_account_details.balance += amount
            recipient_account_details.save()

        label = "sent to" if type == TransactionHistory.transfer else "requested from"
        messages.success(request, f"An Amount of {base_amount} has been {label} {username}")
        return True, username
    else:
        messages.error(request, "you have not sufficient amount for this transaction")
        return False, username


# Create your views here.
def transfer(request):
    if request.user.is_authenticated:
        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        if request.method == "POST":
            validate_recipient = __get_bool(request.POST['validate_recipient'])
            if validate_recipient:
                sufficient_balance, username = __make_transaction(request, TransactionHistory.transfer, validate_recipient)
                if sufficient_balance:
                    return render(request, 'payapp/transfer.html',
                                  {'user': user_data, 'count': notifications_count, 'recipient_user': username,
                                   'validate_recipient': validate_recipient})
            else:
                validate_recipient, username = __verify_user(request, TransactionHistory.transfer, validate_recipient)
                return render(request, 'payapp/transfer.html',
                              {'user': user_data, 'count': notifications_count, 'recipient_user': username,
                               'validate_recipient': validate_recipient})

        validate_recipient = False
        return render(request, 'payapp/transfer.html',
                      {'user': user_data, 'count': notifications_count, 'validate_recipient': validate_recipient})
    return render(request, 'register/SignIn.html')


def send_request(request):
    if request.user.is_authenticated:
        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        if request.method == "POST":
            validate_recipient = __get_bool(request.POST['validate_recipient'])
            if validate_recipient:
                __make_transaction(request, TransactionHistory.request, validate_recipient)
            else:
                validate_recipient, username = __verify_user(request, TransactionHistory.request, validate_recipient)
                return render(request, 'payapp/request.html',
                              {'user': user_data, 'count': notifications_count, 'recipient_user': username,
                               'validate_recipient': validate_recipient})

        validate_recipient = False
        return render(request, 'payapp/request.html',
                      {'user': user_data, 'count': notifications_count, 'validate_recipient': validate_recipient})
    return render(request, 'register/SignIn.html')


def view_transactions(request):
    if request.user.is_authenticated:
        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        if request.user.is_superuser:
            transactions_logs = TransactionHistory.objects.all()
        else:
            transactions_logs = TransactionHistory.objects.filter(
                Q(mode=TransactionHistory.transfer) & (Q(sender=request.user) | Q(receiver=request.user)))

        return render(request, 'payapp/history.html',
                      {'user': user_data, 'count': notifications_count, 'transactions_logs': transactions_logs})

    return render(request, 'register/SignIn.html')


def view_users(request):
    if request.user.is_superuser:
        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        reg_users = UserExtension.objects.all()
        return render(request, 'payapp/users.html',
                      {'user': user_data, 'count': notifications_count, 'reg_users': reg_users})

    return render(request, 'register/SignIn.html')


def notification(request):
    if request.user.is_authenticated:
        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        transactions_logs = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(status=TransactionHistory.pending))

        return render(request, 'payapp/notification_list.html',
                      {'user': user_data, 'count': notifications_count, 'transactions_logs': transactions_logs})

    return render(request, 'register/SignIn.html')


def request_decision(request, id):
    if request.user.is_authenticated:
        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        transaction = TransactionHistory.objects.get(id=id)
        return render(request, 'payapp/request_decision.html',
                      {'user': user_data, 'count': notifications_count, 'transaction': transaction})

    return render(request, 'register/SignIn.html')


def request_action(request, id, decision):
    if request.user.is_authenticated:

        transaction = TransactionHistory.objects.get(id=id)

        if decision == 'accept':
            request_from = transaction.sender
            request_to = transaction.receiver
            amount = transaction.amount
            currency = transaction.currency

            request_amount = amount
            request_user = UserExtension.objects.get(user=request_from)
            donor_user = UserExtension.objects.get(user=request_to)

            if donor_user.currency != currency:
                rate, amount = get_exchange_rate(currency, donor_user.currency, amount)

            if donor_user.balance >= amount:
                TransactionHistory.objects.create(sender=donor_user.user, receiver=request_user.user, amount=request_amount, mode=TransactionHistory.transfer,
                                                  currency=request_user.currency, status=TransactionHistory.completed)

                request_user.balance += request_amount
                request_user.save()

                donor_user.balance -= amount
                donor_user.save()

                transaction.status = TransactionHistory.completed
                transaction.save()

                messages.success(request, "Payment has been Sent Successfully")
                return redirect('payapp:notification')

            messages.error(request, "Your have insufficient amount")
            return redirect('payapp:notification')

        if decision == 'reject':
            transaction.status = TransactionHistory.rejected
            messages.success(request, "Payment Request has been Rejected")
            return redirect('payapp:notification')

    return render(request, 'register/SignIn.html')
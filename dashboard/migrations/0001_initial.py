# Generated by Django 4.0 on 2021-12-20 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='APKFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(null=True)),
                ('apk', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('value', models.CharField(default='', max_length=200)),
                ('category', models.CharField(default='', max_length=200)),
                ('image', models.ImageField(default='', upload_to='dashboard/images/card')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(default=' ', max_length=100)),
                ('walletAmount', models.IntegerField(default=0, null=True)),
                ('openingBalance', models.IntegerField(default=0, null=True)),
                ('status', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default=' ', max_length=300)),
                ('marketType', models.CharField(default=' ', max_length=300)),
                ('rate', models.CharField(default='', max_length=300)),
                ('multipleTimes', models.IntegerField(default=9, null=True)),
                ('status', models.CharField(default='Active', max_length=300)),
                ('remark', models.CharField(default='', max_length=300)),
                ('logo', models.ImageField(default='', upload_to='dashboard/game/logo')),
            ],
        ),
        migrations.CreateModel(
            name='JodiMarket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default=' ', max_length=300)),
                ('closeTime', models.CharField(default='', max_length=100)),
                ('result', models.CharField(default='**', max_length=300)),
                ('status', models.CharField(default='Game running now', max_length=300)),
                ('remark', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default=' ', max_length=300)),
                ('openTime', models.CharField(default='', max_length=100)),
                ('closeTime', models.CharField(default='', max_length=100)),
                ('status', models.CharField(default='Game running now', max_length=300)),
                ('rummyResultOpen', models.TextField(default='***')),
                ('rummyResultClose', models.TextField(default='***')),
                ('jokerResultOpen', models.TextField(default='*')),
                ('jokerResultClose', models.TextField(default='*')),
                ('remark', models.CharField(default=' ', max_length=300)),
                ('updateDate', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(default=' ', max_length=100)),
                ('city', models.CharField(default=' ', max_length=100)),
                ('address', models.TextField(default=' ')),
                ('panNumber', models.CharField(default=' ', max_length=100)),
                ('bankName', models.CharField(default=' ', max_length=100)),
                ('accountNumber', models.CharField(default=' ', max_length=100)),
                ('ifscCode', models.CharField(default=' ', max_length=100)),
                ('earningAmount', models.IntegerField(default=0, null=True)),
                ('commision', models.IntegerField(default=2, null=True)),
                ('walletAmount', models.IntegerField(default=0, null=True)),
                ('openingBalance', models.IntegerField(default=0, null=True)),
                ('totalBiddingAmount', models.IntegerField(default=0, null=True)),
                ('payingBiddingAmount', models.IntegerField(default=0, null=True)),
                ('status', models.CharField(default='Acitve', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Rulls',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=300)),
                ('msg', models.CharField(default='', max_length=500)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='Placed', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='New', max_length=200)),
                ('remark', models.CharField(default='New Withdraw request', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
        migrations.CreateModel(
            name='UserRoll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('roll', models.CharField(default='', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('transactionType', models.CharField(default='', max_length=300)),
                ('transactionMode', models.CharField(default='', max_length=300)),
                ('signature', models.CharField(default='', max_length=300)),
                ('successPaymentId', models.CharField(default='', max_length=300)),
                ('successOrderId', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='success', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
        migrations.CreateModel(
            name='TopWinner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('digit', models.IntegerField(default=0, null=True)),
                ('points', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('status', models.CharField(default='Placed', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PartnerWithdraw',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('biddingAmount', models.IntegerField(default=0, null=True)),
                ('commision', models.IntegerField(default=2, null=True)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='New', max_length=200)),
                ('remark', models.CharField(default='New Withdraw request', max_length=200)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.partner')),
            ],
        ),
        migrations.CreateModel(
            name='PartnerUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='Acitve', max_length=200)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.partner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
        migrations.CreateModel(
            name='PanelChartRegulerMarket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('openThreeDigit', models.CharField(default='***', max_length=100)),
                ('closeThreeDigit', models.CharField(default='***', max_length=100)),
                ('openSingleDigit', models.CharField(default='***', max_length=100)),
                ('CloseSingleDigit', models.CharField(default='***', max_length=100)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='Closed', max_length=200)),
                ('remark', models.CharField(default='Previous Result', max_length=200)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.market')),
            ],
        ),
        migrations.CreateModel(
            name='PanelChartJodiMarket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resultDigit', models.CharField(default='**', max_length=100)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='Closed', max_length=200)),
                ('remark', models.CharField(default='Previous Result', max_length=200)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.jodimarket')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=300)),
                ('msg', models.CharField(default='', max_length=500)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='Placed', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
        migrations.CreateModel(
            name='JodiTopWinner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('digit', models.IntegerField(default=0, null=True)),
                ('points', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('status', models.CharField(default='Placed', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
        migrations.CreateModel(
            name='JodiBiddingHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('digit', models.CharField(default='', max_length=30)),
                ('winAmount', models.IntegerField(default=0, null=True)),
                ('points', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('status', models.CharField(default='Placed', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.games')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.jodimarket')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='roll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.userroll'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.CreateModel(
            name='BiddingHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rummyCard', models.TextField(default='***')),
                ('jokerCard', models.TextField(default='*')),
                ('winAmount', models.IntegerField(default=0, null=True)),
                ('points', models.CharField(default='', max_length=300)),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('status', models.CharField(default='', max_length=200)),
                ('marketType', models.CharField(default='', max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.games')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.market')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accountNumber', models.CharField(default='0', max_length=100)),
                ('ifscCode', models.CharField(default='', max_length=300)),
                ('bankName', models.CharField(default='', max_length=300)),
                ('accountName', models.CharField(default='', max_length=300)),
                ('status', models.CharField(default='', max_length=200)),
                ('date', models.DateField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer')),
            ],
        ),
    ]

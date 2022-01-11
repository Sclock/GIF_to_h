a = ['hutao_1.jpg', 'hutao_10.jpg', 'hutao_11.jpg', 'hutao_12.jpg', 'hutao_13.jpg', 'hutao_14.jpg', 'hutao_15.jpg', 'hutao_16.jpg', 'hutao_17.jpg', 'hutao_18.jpg', 'hutao_19.jpg', 'hutao_2.jpg', 'hutao_20.jpg', 'hutao_21.jpg', 'hutao_22.jpg', 'hutao_23.jpg',
     'hutao_24.jpg', 'hutao_25.jpg', 'hutao_26.jpg', 'hutao_27.jpg', 'hutao_28.jpg', 'hutao_29.jpg', 'hutao_3.jpg', 'hutao_30.jpg', 'hutao_31.jpg', 'hutao_32.jpg', 'hutao_4.jpg', 'hutao_5.jpg', 'hutao_6.jpg', 'hutao_7.jpg', 'hutao_8.jpg', 'hutao_9.jpg']
a.sort(key=lambda x: int(x.split('.')[0].split('_')[1]))

b = [5, 15, 2, 3, 21, 22, 35, 3, 5, 9]
b.sort()
print(a)

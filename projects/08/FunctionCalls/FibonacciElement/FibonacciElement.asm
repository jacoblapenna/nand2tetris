// this is the bootstrap code block
@256                                                                // 0
D=A                                                                 // 1
@SP                                                                 // 2
M=D                                                                 // 3
// call sys.init 0
@sys.init.return_0                                                  // 4
D=A                                                                 // 5
@SP                                                                 // 6
A=M                                                                 // 7
M=D                                                                 // 8
@SP                                                                 // 9
M=M+1                                                               // 10
@LCL                                                                // 11
D=M                                                                 // 12
@SP                                                                 // 13
A=M                                                                 // 14
M=D                                                                 // 15
@SP                                                                 // 16
M=M+1                                                               // 17
@ARG                                                                // 18
D=M                                                                 // 19
@SP                                                                 // 20
A=M                                                                 // 21
M=D                                                                 // 22
@SP                                                                 // 23
M=M+1                                                               // 24
@THIS                                                               // 25
D=M                                                                 // 26
@SP                                                                 // 27
A=M                                                                 // 28
M=D                                                                 // 29
@SP                                                                 // 30
M=M+1                                                               // 31
@THAT                                                               // 32
D=M                                                                 // 33
@SP                                                                 // 34
A=M                                                                 // 35
M=D                                                                 // 36
@SP                                                                 // 37
M=M+1                                                               // 38
@SP                                                                 // 39
D=M                                                                 // 40
@5                                                                  // 41
D=D-A                                                               // 42
@0                                                                  // 43
D=D-A                                                               // 44
@ARG                                                                // 45
M=D                                                                 // 46
@SP                                                                 // 47
D=M                                                                 // 48
@LCL                                                                // 49
M=D                                                                 // 50
@sys.init                                                           // 51
0;JMP                                                               // 52
(sys.init.return_0)
// function main.fibonacci 0
(main.fibonacci)
// push argument 0
@0                                                                  // 53
D=A                                                                 // 54
@ARG                                                                // 55
A=D+M                                                               // 56
D=M                                                                 // 57
@SP                                                                 // 58
A=M                                                                 // 59
M=D                                                                 // 60
@SP                                                                 // 61
M=M+1                                                               // 62
// push constant 2
@2                                                                  // 63
D=A                                                                 // 64
@SP                                                                 // 65
A=M                                                                 // 66
M=D                                                                 // 67
@SP                                                                 // 68
M=M+1                                                               // 69
// lt
@SP                                                                 // 70
M=M-1                                                               // 71
@SP                                                                 // 72
A=M                                                                 // 73
D=M                                                                 // 74
@SP                                                                 // 75
M=M-1                                                               // 76
@SP                                                                 // 77
A=M                                                                 // 78
M=M-D                                                               // 79
@SP                                                                 // 80
A=M                                                                 // 81
D=M                                                                 // 82
@LESS_THAN0                                                         // 83
D;JLT                                                               // 84
@NOT_LESS_THAN0                                                     // 85
0;JMP                                                               // 86
(LESS_THAN0)
@SP                                                                 // 87
A=M                                                                 // 88
M=-1                                                                // 89
@LT_FINISH0                                                         // 90
0;JMP                                                               // 91
(NOT_LESS_THAN0)
@SP                                                                 // 92
A=M                                                                 // 93
M=0                                                                 // 94
@LT_FINISH0                                                         // 95
0;JMP                                                               // 96
(LT_FINISH0)
@SP                                                                 // 97
M=M+1                                                               // 98
// if-goto if_true
@SP                                                                 // 99
M=M-1                                                               // 100
A=M                                                                 // 101
D=M                                                                 // 102
@if_true                                                            // 103
D;JNE                                                               // 104
// goto if_false
@if_false                                                           // 105
0;JMP                                                               // 106
// label if_true
(if_true)
// push argument 0
@0                                                                  // 107
D=A                                                                 // 108
@ARG                                                                // 109
A=D+M                                                               // 110
D=M                                                                 // 111
@SP                                                                 // 112
A=M                                                                 // 113
M=D                                                                 // 114
@SP                                                                 // 115
M=M+1                                                               // 116
// return
@5                                                                  // 117
D=A                                                                 // 118
@LCL                                                                // 119
D=M-D                                                               // 120
A=D                                                                 // 121
D=M                                                                 // 122
@R14                                                                // 123
M=D                                                                 // 124
@0                                                                  // 125
D=A                                                                 // 126
@ARG                                                                // 127
A=D+M                                                               // 128
D=A                                                                 // 129
@R13                                                                // 130
M=D                                                                 // 131
@SP                                                                 // 132
M=M-1                                                               // 133
A=M                                                                 // 134
D=M                                                                 // 135
@R13                                                                // 136
A=M                                                                 // 137
M=D                                                                 // 138
@ARG                                                                // 139
D=M+1                                                               // 140
@SP                                                                 // 141
M=D                                                                 // 142
@LCL                                                                // 143
M=M-1                                                               // 144
@LCL                                                                // 145
A=M                                                                 // 146
D=M                                                                 // 147
@THAT                                                               // 148
M=D                                                                 // 149
@LCL                                                                // 150
M=M-1                                                               // 151
@LCL                                                                // 152
A=M                                                                 // 153
D=M                                                                 // 154
@THIS                                                               // 155
M=D                                                                 // 156
@LCL                                                                // 157
M=M-1                                                               // 158
@LCL                                                                // 159
A=M                                                                 // 160
D=M                                                                 // 161
@ARG                                                                // 162
M=D                                                                 // 163
@LCL                                                                // 164
M=M-1                                                               // 165
@LCL                                                                // 166
A=M                                                                 // 167
D=M                                                                 // 168
@LCL                                                                // 169
M=D                                                                 // 170
@R14                                                                // 171
A=M                                                                 // 172
0;JMP                                                               // 173
// label if_false
(if_false)
// push argument 0
@0                                                                  // 174
D=A                                                                 // 175
@ARG                                                                // 176
A=D+M                                                               // 177
D=M                                                                 // 178
@SP                                                                 // 179
A=M                                                                 // 180
M=D                                                                 // 181
@SP                                                                 // 182
M=M+1                                                               // 183
// push constant 2
@2                                                                  // 184
D=A                                                                 // 185
@SP                                                                 // 186
A=M                                                                 // 187
M=D                                                                 // 188
@SP                                                                 // 189
M=M+1                                                               // 190
// sub
@SP                                                                 // 191
M=M-1                                                               // 192
@SP                                                                 // 193
A=M                                                                 // 194
D=M                                                                 // 195
@SP                                                                 // 196
M=M-1                                                               // 197
@SP                                                                 // 198
A=M                                                                 // 199
M=M-D                                                               // 200
@SP                                                                 // 201
M=M+1                                                               // 202
// call main.fibonacci 1
@main.fibonacci.return_1                                            // 203
D=A                                                                 // 204
@SP                                                                 // 205
A=M                                                                 // 206
M=D                                                                 // 207
@SP                                                                 // 208
M=M+1                                                               // 209
@LCL                                                                // 210
D=M                                                                 // 211
@SP                                                                 // 212
A=M                                                                 // 213
M=D                                                                 // 214
@SP                                                                 // 215
M=M+1                                                               // 216
@ARG                                                                // 217
D=M                                                                 // 218
@SP                                                                 // 219
A=M                                                                 // 220
M=D                                                                 // 221
@SP                                                                 // 222
M=M+1                                                               // 223
@THIS                                                               // 224
D=M                                                                 // 225
@SP                                                                 // 226
A=M                                                                 // 227
M=D                                                                 // 228
@SP                                                                 // 229
M=M+1                                                               // 230
@THAT                                                               // 231
D=M                                                                 // 232
@SP                                                                 // 233
A=M                                                                 // 234
M=D                                                                 // 235
@SP                                                                 // 236
M=M+1                                                               // 237
@SP                                                                 // 238
D=M                                                                 // 239
@5                                                                  // 240
D=D-A                                                               // 241
@1                                                                  // 242
D=D-A                                                               // 243
@ARG                                                                // 244
M=D                                                                 // 245
@SP                                                                 // 246
D=M                                                                 // 247
@LCL                                                                // 248
M=D                                                                 // 249
@main.fibonacci                                                     // 250
0;JMP                                                               // 251
(main.fibonacci.return_1)
// push argument 0
@0                                                                  // 252
D=A                                                                 // 253
@ARG                                                                // 254
A=D+M                                                               // 255
D=M                                                                 // 256
@SP                                                                 // 257
A=M                                                                 // 258
M=D                                                                 // 259
@SP                                                                 // 260
M=M+1                                                               // 261
// push constant 1
@1                                                                  // 262
D=A                                                                 // 263
@SP                                                                 // 264
A=M                                                                 // 265
M=D                                                                 // 266
@SP                                                                 // 267
M=M+1                                                               // 268
// sub
@SP                                                                 // 269
M=M-1                                                               // 270
@SP                                                                 // 271
A=M                                                                 // 272
D=M                                                                 // 273
@SP                                                                 // 274
M=M-1                                                               // 275
@SP                                                                 // 276
A=M                                                                 // 277
M=M-D                                                               // 278
@SP                                                                 // 279
M=M+1                                                               // 280
// call main.fibonacci 1
@main.fibonacci.return_2                                            // 281
D=A                                                                 // 282
@SP                                                                 // 283
A=M                                                                 // 284
M=D                                                                 // 285
@SP                                                                 // 286
M=M+1                                                               // 287
@LCL                                                                // 288
D=M                                                                 // 289
@SP                                                                 // 290
A=M                                                                 // 291
M=D                                                                 // 292
@SP                                                                 // 293
M=M+1                                                               // 294
@ARG                                                                // 295
D=M                                                                 // 296
@SP                                                                 // 297
A=M                                                                 // 298
M=D                                                                 // 299
@SP                                                                 // 300
M=M+1                                                               // 301
@THIS                                                               // 302
D=M                                                                 // 303
@SP                                                                 // 304
A=M                                                                 // 305
M=D                                                                 // 306
@SP                                                                 // 307
M=M+1                                                               // 308
@THAT                                                               // 309
D=M                                                                 // 310
@SP                                                                 // 311
A=M                                                                 // 312
M=D                                                                 // 313
@SP                                                                 // 314
M=M+1                                                               // 315
@SP                                                                 // 316
D=M                                                                 // 317
@5                                                                  // 318
D=D-A                                                               // 319
@1                                                                  // 320
D=D-A                                                               // 321
@ARG                                                                // 322
M=D                                                                 // 323
@SP                                                                 // 324
D=M                                                                 // 325
@LCL                                                                // 326
M=D                                                                 // 327
@main.fibonacci                                                     // 328
0;JMP                                                               // 329
(main.fibonacci.return_2)
// add
@SP                                                                 // 330
M=M-1                                                               // 331
@SP                                                                 // 332
A=M                                                                 // 333
D=M                                                                 // 334
@SP                                                                 // 335
M=M-1                                                               // 336
@SP                                                                 // 337
A=M                                                                 // 338
M=M+D                                                               // 339
@SP                                                                 // 340
M=M+1                                                               // 341
// return
@5                                                                  // 342
D=A                                                                 // 343
@LCL                                                                // 344
D=M-D                                                               // 345
A=D                                                                 // 346
D=M                                                                 // 347
@R14                                                                // 348
M=D                                                                 // 349
@0                                                                  // 350
D=A                                                                 // 351
@ARG                                                                // 352
A=D+M                                                               // 353
D=A                                                                 // 354
@R13                                                                // 355
M=D                                                                 // 356
@SP                                                                 // 357
M=M-1                                                               // 358
A=M                                                                 // 359
D=M                                                                 // 360
@R13                                                                // 361
A=M                                                                 // 362
M=D                                                                 // 363
@ARG                                                                // 364
D=M+1                                                               // 365
@SP                                                                 // 366
M=D                                                                 // 367
@LCL                                                                // 368
M=M-1                                                               // 369
@LCL                                                                // 370
A=M                                                                 // 371
D=M                                                                 // 372
@THAT                                                               // 373
M=D                                                                 // 374
@LCL                                                                // 375
M=M-1                                                               // 376
@LCL                                                                // 377
A=M                                                                 // 378
D=M                                                                 // 379
@THIS                                                               // 380
M=D                                                                 // 381
@LCL                                                                // 382
M=M-1                                                               // 383
@LCL                                                                // 384
A=M                                                                 // 385
D=M                                                                 // 386
@ARG                                                                // 387
M=D                                                                 // 388
@LCL                                                                // 389
M=M-1                                                               // 390
@LCL                                                                // 391
A=M                                                                 // 392
D=M                                                                 // 393
@LCL                                                                // 394
M=D                                                                 // 395
@R14                                                                // 396
A=M                                                                 // 397
0;JMP                                                               // 398
// function sys.init 0
(sys.init)
// push constant 4
@4                                                                  // 399
D=A                                                                 // 400
@SP                                                                 // 401
A=M                                                                 // 402
M=D                                                                 // 403
@SP                                                                 // 404
M=M+1                                                               // 405
// call main.fibonacci 1
@main.fibonacci.return_3                                            // 406
D=A                                                                 // 407
@SP                                                                 // 408
A=M                                                                 // 409
M=D                                                                 // 410
@SP                                                                 // 411
M=M+1                                                               // 412
@LCL                                                                // 413
D=M                                                                 // 414
@SP                                                                 // 415
A=M                                                                 // 416
M=D                                                                 // 417
@SP                                                                 // 418
M=M+1                                                               // 419
@ARG                                                                // 420
D=M                                                                 // 421
@SP                                                                 // 422
A=M                                                                 // 423
M=D                                                                 // 424
@SP                                                                 // 425
M=M+1                                                               // 426
@THIS                                                               // 427
D=M                                                                 // 428
@SP                                                                 // 429
A=M                                                                 // 430
M=D                                                                 // 431
@SP                                                                 // 432
M=M+1                                                               // 433
@THAT                                                               // 434
D=M                                                                 // 435
@SP                                                                 // 436
A=M                                                                 // 437
M=D                                                                 // 438
@SP                                                                 // 439
M=M+1                                                               // 440
@SP                                                                 // 441
D=M                                                                 // 442
@5                                                                  // 443
D=D-A                                                               // 444
@1                                                                  // 445
D=D-A                                                               // 446
@ARG                                                                // 447
M=D                                                                 // 448
@SP                                                                 // 449
D=M                                                                 // 450
@LCL                                                                // 451
M=D                                                                 // 452
@main.fibonacci                                                     // 453
0;JMP                                                               // 454
(main.fibonacci.return_3)
// label while
(while)
// goto while
@while                                                              // 455
0;JMP                                                               // 456
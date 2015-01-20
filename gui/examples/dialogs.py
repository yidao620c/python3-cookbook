#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 对话框
    Desc : 
"""
__author__ = 'Xiong Neng'
import wx


def main():
    app = wx.App()
    # --------------------确认对话框--------------------------
    # dlg = wx.MessageDialog(None, 'Is this the coolest thing ever!',
    # 'MessageDialog', wx.YES_NO | wx.ICON_QUESTION)
    # # wx.ID_YES, wx.ID_NO, wx.ID_CANCEL, wx.ID_OK
    # result = dlg.ShowModal()
    # ---------------------文本输入对话框-----------------------
    # dlg = wx.TextEntryDialog(None, "Who is buried in Grant's tomb?",
    # 'A Question', 'Cary Grant')
    # if dlg.ShowModal() == wx.ID_OK:
    #     response = dlg.GetValue()
    # ---------------------列表选择对话框-----------------------
    dlg = wx.SingleChoiceDialog(None,
                                'What version of Python are you using?',
                                'Single Choice',
                                ['1.5.2', '2.0', '2.6.3', '2.7', '2.7.8'])
    if dlg.ShowModal() == wx.ID_OK:
        response = dlg.GetStringSelection()
        print(response)
    app.MainLoop()


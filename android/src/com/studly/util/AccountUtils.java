package com.studly.util;

import java.util.Arrays;
import java.util.List;

import android.accounts.Account;
import android.accounts.AccountManager;
import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.text.TextUtils;
import android.util.Log;

public final class AccountUtils {

    private static final String TAG = "AccountUtils";
    private static final String PREF_CHOSEN_ACCOUNT = "chosen_account";

    public static final String GOOGLE_ACCOUNT_TYPE = "com.google";

    private AccountUtils() {
    }

    public static List<Account> getAccounts(final Context context) {
        AccountManager accountManager = AccountManager.get(context);
        return Arrays.asList(accountManager.getAccountsByType(GOOGLE_ACCOUNT_TYPE));
    }

    public static String getChosenAccountName(final Context context) {
        SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
        return sp.getString(PREF_CHOSEN_ACCOUNT, null);
    }
    
    public static boolean isAuthenticated(final Context context) {
        return !TextUtils.isEmpty(getChosenAccountName(context));
    }

    public static void setChosenAccountName(final Context context, final String accountName) {
        Log.d(TAG, "Chose account " + accountName);
        SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
        sp.edit().putString(PREF_CHOSEN_ACCOUNT, accountName).commit();
    }
}

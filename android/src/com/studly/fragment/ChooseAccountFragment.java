package com.studly.fragment;

import java.util.ArrayList;
import java.util.List;

import android.accounts.Account;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.DialogInterface;
import android.os.Bundle;

import com.studly.R;
import com.studly.util.AccountUtils;

public class ChooseAccountFragment extends DialogFragment {

    public interface ChooseAccountListener {
        void onAccountChosen(final Account account);
    }

    private ChooseAccountListener mListener;
    private List<Account> mAccounts;

    public ChooseAccountFragment() {
    }

    public static ChooseAccountFragment newInstance(ChooseAccountListener listener) {
        ChooseAccountFragment accountChooser = new ChooseAccountFragment();
        accountChooser.mListener = listener;
        return accountChooser;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mAccounts = AccountUtils.getAccounts(getActivity());
    }

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        builder.setTitle(R.string.choose_account_text);
        ArrayList<String> emails = new ArrayList<String>();
        for (Account account : mAccounts) {
            emails.add(account.name);
        }
        builder.setItems(emails.toArray(new String[0]), new DialogInterface.OnClickListener() {

            @Override
            public void onClick(DialogInterface dialog, int which) {
                mListener.onAccountChosen(mAccounts.get(which));
            }
        });
        return builder.create();
    }
}

package com.studly.fragment;

import java.util.ArrayList;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.content.ContentResolver;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.CalendarContract.Calendars;

import com.studly.R;

public class ChooseGroupFragment extends DialogFragment {

    // Projection array. Creating indices for this array instead of doing
    // dynamic lookups improves performance.
    public static final String[] EVENT_PROJECTION = new String[] { 
            Calendars._ID, // 0
            Calendars.ACCOUNT_NAME, // 1
            Calendars.CALENDAR_DISPLAY_NAME, // 2
            Calendars.OWNER_ACCOUNT // 3
    };

    // The indices for the projection array above.
    private static final int PROJECTION_ID_INDEX = 0;
    private static final int PROJECTION_ACCOUNT_NAME_INDEX = 1;
    private static final int PROJECTION_DISPLAY_NAME_INDEX = 2;
    private static final int PROJECTION_OWNER_ACCOUNT_INDEX = 3;

    public interface ChooseGroupListener {
        void onGroupChosen(long calId);
    }

    private ChooseGroupListener mListener;

    public static ChooseGroupFragment newInstance(ChooseGroupListener listener) {
        ChooseGroupFragment newGroup = new ChooseGroupFragment();
        newGroup.mListener = listener;
        return newGroup;
    }

    public ChooseGroupFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        // Run query
        Cursor cur = null;
        ContentResolver cr = getActivity().getContentResolver();
        Uri uri = Calendars.CONTENT_URI;
        cur = cr.query(uri, EVENT_PROJECTION, null, null, null);

        ArrayList<String> groups = new ArrayList<String>();
        ArrayList<Long> calIds = new ArrayList<Long>();
        while (cur.moveToNext()) {
            long calID = 0;
            String displayName = null;

            // Get the field values
            calID = cur.getLong(PROJECTION_ID_INDEX);
            displayName = cur.getString(PROJECTION_DISPLAY_NAME_INDEX);
            groups.add(displayName);
            calIds.add(calID);
        }

        final Long[] idArray = calIds.toArray(new Long[calIds.size()]);
        AlertDialog.Builder alert = new AlertDialog.Builder(getActivity());
        alert.setTitle(R.string.choose_group_text);
        alert.setItems(groups.toArray(new String[0]), new OnClickListener() {

            @Override
            public void onClick(DialogInterface dialog, int which) {
                mListener.onGroupChosen(idArray[which]);
            }
        });
        return alert.create();
    }

}

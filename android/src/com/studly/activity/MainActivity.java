package com.studly.activity;

import android.accounts.Account;
import android.app.ListActivity;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.octo.android.robospice.SpiceManager;
import com.octo.android.robospice.persistence.exception.SpiceException;
import com.octo.android.robospice.request.listener.RequestListener;
import com.studly.R;
import com.studly.fragment.ChooseAccountFragment;
import com.studly.fragment.ChooseAccountFragment.ChooseAccountListener;
import com.studly.fragment.ChooseGroupFragment;
import com.studly.fragment.ChooseGroupFragment.ChooseGroupListener;
import com.studly.model.StudlyMapping;
import com.studly.network.RequestJoinGroup;
import com.studly.network.RequestStudlyGroups;
import com.studly.service.StudlyService;
import com.studly.util.AccountUtils;

public class MainActivity extends ListActivity implements ChooseAccountListener, ChooseGroupListener {

    private static final String TAG = "MainActivity";
    private static final String CHOOSE_ACCOUNT_TAG = "account_chooser";
    private static final String CHOOSE_EVENT_TAG = "event_chooser";
    private static final String KEY_CHOSEN_ACCOUNT = "chosen_account";

    /* Attributes */

    private SpiceManager mSpiceManager = new SpiceManager(StudlyService.class);
    private String mAccountName;
    private RequestStudlyGroups mRequestStudlyGroups;
    private StudlyAdapter mStudlyAdapter;

    /* Methods */

    private void performRequest() {
        mSpiceManager.execute(mRequestStudlyGroups, new StudlyMappingRequestListener());
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (!AccountUtils.isAuthenticated(this)) {
            ChooseAccountFragment.newInstance(this).show(getFragmentManager(), CHOOSE_ACCOUNT_TAG);
        }

        if (savedInstanceState != null) {
            mAccountName = savedInstanceState.getString(KEY_CHOSEN_ACCOUNT);
        } else {
            mAccountName = AccountUtils.getChosenAccountName(this);
        }

        mRequestStudlyGroups = new RequestStudlyGroups();
        try {
            Log.d(TAG, "Setting list adapter");
            performRequest();
            setListAdapter(mStudlyAdapter);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case R.id.action_new_event:
            ChooseGroupFragment.newInstance(this).show(getFragmentManager(), CHOOSE_EVENT_TAG);
            return true;
        default:
            return super.onOptionsItemSelected(item);
        }
    }

    @Override
    protected void onStart() {
        super.onStart();
        mSpiceManager.start(this);
    }

    @Override
    protected void onStop() {
        mSpiceManager.shouldStop();
        super.onStop();
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        if (mAccountName != null) {
            outState.putString(KEY_CHOSEN_ACCOUNT, mAccountName);
        }
        super.onSaveInstanceState(outState);
    }

    @Override
    public void onAccountChosen(Account account) {
        AccountUtils.setChosenAccountName(this, account.name);
    }

    @Override
    public void onGroupChosen(long calId) {
        Toast.makeText(this, "Event title " + calId, Toast.LENGTH_SHORT).show();
    }

    /* Classes */

    private class StudlyAdapter extends ArrayAdapter<StudlyMapping> {

        public StudlyAdapter(Context context, StudlyMapping.List events) {
            super(context, 0, events);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            Log.d(TAG, "Create new view");
            LayoutInflater inflater = getLayoutInflater();
            View view = inflater.inflate(R.layout.studly_list_item, null);

            final StudlyMapping mapping = getItem(position);
            if (mapping != null) {
                Log.d(TAG, "creating row for event " + mapping.getTitle() + " calendar " + mapping.getCalendarId());

                TextView textView = (TextView) view.findViewById(R.id.row_event);
                textView.setText(mapping.getTitle());

                Button join = (Button) view.findViewById(R.id.button_join);
                join.setOnClickListener(new OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        RequestJoinGroup request = new RequestJoinGroup(mapping, AccountUtils
                                .getChosenAccountName(MainActivity.this));
                        mSpiceManager.execute(request, new StudlyJoinRequestListener());
                    }
                });
            }
            return view;
        }

    }

    private class StudlyJoinRequestListener implements RequestListener<StudlyMapping> {

        @Override
        public void onRequestFailure(SpiceException spiceException) {
        }

        @Override
        public void onRequestSuccess(StudlyMapping mapping) {
            performRequest();
        }

    }

    private class StudlyMappingRequestListener implements RequestListener<StudlyMapping.List> {

        @Override
        public void onRequestFailure(SpiceException spiceException) {
        }

        @Override
        public void onRequestSuccess(StudlyMapping.List groups) {
            mStudlyAdapter = new StudlyAdapter(MainActivity.this, groups);
            setListAdapter(mStudlyAdapter);
        }

    }

}

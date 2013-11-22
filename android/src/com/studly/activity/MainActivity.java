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
import com.studly.R;
import com.studly.fragment.ChooseAccountFragment;
import com.studly.fragment.ChooseAccountFragment.ChooseAccountListener;
import com.studly.fragment.ChooseGroupFragment;
import com.studly.fragment.ChooseGroupFragment.ChooseGroupListener;
import com.studly.model.StudlyEvent;
import com.studly.network.RequestStudlyEvents;
import com.studly.service.StudlyService;
import com.studly.util.AccountUtils;

public class MainActivity extends ListActivity implements ChooseAccountListener, ChooseGroupListener {

    private static final String TAG = "MainActivity";
    private static final String CHOOSE_ACCOUNT_TAG = "account_chooser";
    private static final String CHOOSE_EVENT_TAG = "event_chooser";
    private static final String KEY_CHOSEN_ACCOUNT = "chosen_account";

    /* Attributes */

    private String mAccountName;
    private SpiceManager mSpiceManager = new SpiceManager(StudlyService.class);
    private RequestStudlyEvents mRequestStudlyEvents;

    class StudlyAdapter extends ArrayAdapter<StudlyEvent> {

        public StudlyAdapter(Context context, StudlyEvent.List events) {
            super(context, 0, events);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            Log.d(TAG, "Create new view");
            LayoutInflater inflater = getLayoutInflater();
            View view = inflater.inflate(R.layout.studly_list_item, null);

            StudlyEvent event = getItem(position);
            if (event != null) {
                Log.d(TAG, "creating row for event " + event.getName());

                TextView textView = (TextView) view.findViewById(R.id.row_event);
                textView.setText(event.getName());

                Button join = (Button) view.findViewById(R.id.button_join);
                join.setText(event.isJoined() ? "Join" : "Leave");
                join.setOnClickListener(new JoinClickListener(event));
            }
            return view;
        }

    }

    class JoinClickListener implements OnClickListener {

        private StudlyEvent event;

        public JoinClickListener(StudlyEvent event) {
            this.event = event;
        }

        @Override
        public void onClick(View v) {
            if (event.isJoined()) {
                Toast.makeText(MainActivity.this, "Join " + event.getName(), Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(MainActivity.this, "Leave " + event.getName(), Toast.LENGTH_SHORT).show();
            }
            // mSpiceManager.execute(request, requestListener);
        }

    }

    /* Methods */

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

        mRequestStudlyEvents = new RequestStudlyEvents();
        try {
            Log.d(TAG, "Setting list adapter");
            // mSpiceManager.execute(mRequestStudlyEvents, requestListener);
            setListAdapter(new StudlyAdapter(this, mRequestStudlyEvents.loadDataFromNetwork()));
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

}

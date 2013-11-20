package com.studly.activity;

import android.app.ListActivity;
import android.content.Context;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.octo.android.robospice.SpiceManager;
import com.studly.R;
import com.studly.model.StudlyEvent;
import com.studly.network.RequestStudlyEvents;
import com.studly.service.StudlyService;
import com.studly.util.AccountUtils;

public class MainActivity extends ListActivity {

    private static final String TAG = "MainActivity";

    /* Attributes */

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
            final String account = AccountUtils.getChosenAccountName(MainActivity.this);
            if (TextUtils.isEmpty(account)) {
                // TODO set chosen account
            }
            //mSpiceManager.execute(request, requestListener);
        }

    }

    /* Methods */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mRequestStudlyEvents = new RequestStudlyEvents();
        try {
            Log.d(TAG, "Setting list adapter");
            //mSpiceManager.execute(mRequestStudlyEvents, requestListener);
            setListAdapter(new StudlyAdapter(this, mRequestStudlyEvents.loadDataFromNetwork()));
        } catch (Exception e) {
            e.printStackTrace();
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

}
